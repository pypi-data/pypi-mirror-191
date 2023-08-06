import numpy as np

import torch
import torch.nn as nn
from typing import Any
from torchdiffeq import odeint_adjoint as odeint

from hydroforecast.exp.torch_exp import TorchLearner
from hydroforecast.loader.base_module import TorchDataset
from hydroforecast.models.torch_models import BaseTorchModel
from hydroforecast.optimization import SearchParam

step_fct = lambda x: (torch.tanh(5.0 * x) + 1.0) * 0.5
Ps = lambda P, T, Tmin: step_fct(Tmin - T) * P
Pr = lambda P, T, Tmin: step_fct(T - Tmin) * P
M = lambda S0, T, Df, Tmax: step_fct(T - Tmax) * step_fct(S0) * torch.minimum(S0, Df * (T - Tmax))
PET = lambda T, Lday: 29.8 * Lday * 0.611 * torch.exp((17.3 * T) / (T + 237.3)) / (T + 273.2)
ET = lambda S1, T, Lday, Smax: step_fct(S1) * step_fct(S1 - Smax) * PET(T, Lday) + \
                               step_fct(S1) * step_fct(Smax - S1) * PET(T, Lday) * (S1 / Smax)
Qb = lambda S1, f, Smax, Qmax: step_fct(S1) * step_fct(S1 - Smax) * Qmax + step_fct(S1) * step_fct(
    Smax - S1) * Qmax * torch.exp(-f * (Smax - S1))
Qs = lambda S1, Smax: step_fct(S1) * step_fct(S1 - Smax) * (S1 - Smax)


class PretrainDataset(TorchDataset):
    def __len__(self):
        return len(self.feature)

    def __getitem__(self, i):
        if i >= len(self):
            return ValueError()
        x = torch.from_numpy(self.feature[i, :].astype(np.float32)).to(self.device)
        y = torch.from_numpy(self.target[i, :].astype(np.float32)).to(self.device)
        return x, y


class ODEFuncDataset(TorchDataset):
    means = None
    stds = None

    def __init__(self, slide_window, lead_time, means, stds, device=torch.device('cpu'), feature=None, target=None):
        super().__init__(slide_window, lead_time, device, feature, target)
        self.means = means
        self.stds = stds

    def __len__(self):
        return len(self.feature)

    @classmethod
    def set_data(cls, feature, target, dataset):
        # required before training
        return cls(slide_window=dataset.slide_window, lead_time=dataset.lead_time,
                   device=dataset.device, means=dataset.means,
                   stds=dataset.stds, feature=feature, target=target)

    def __getitem__(self, i):
        if i >= len(self):
            return ValueError()
        ode_input = torch.from_numpy((self.feature[i, 2:5] * self.stds.values
                                      + self.means.values).astype(np.float32)).to(self.device)
        x = torch.from_numpy(self.feature[i, :].astype(np.float32)).to(self.device)
        y = torch.from_numpy(self.target[i, :].astype(np.float32)).to(self.device)
        return x, ode_input, y


def rms_norm(tensor):
    return tensor.pow(2).mean().sqrt()


def make_norm(state):
    state_size = state.numel()

    def norm(aug_state):
        y = aug_state[1:1 + state_size]
        adj_y = aug_state[1 + state_size:1 + 2 * state_size]
        return max(rms_norm(y), rms_norm(adj_y))

    return norm


class M50_NN(BaseTorchModel):
    model_params = [SearchParam(name='hidden_units', dtype='int', low=16, high=32, step=8, default=16)]

    def __init__(self, input_dim, output_dim, slide_window, hidden_units=16):
        super(M50_NN, self).__init__(input_dim, output_dim, slide_window)
        self.model = nn.Sequential(nn.Linear(in_features=input_dim, out_features=hidden_units),
                                   nn.Tanh(),
                                   nn.Linear(in_features=hidden_units, out_features=hidden_units),
                                   nn.LeakyReLU(),
                                   nn.Linear(in_features=hidden_units, out_features=output_dim))

    def forward(self, x):
        x = self.model(x).squeeze()
        return x


class M50_ODEFunc(BaseTorchModel):
    def __init__(self, input_dim, output_dim, slide_window, ET_net, Q_net, f, Smax, Qmax, Df, Tmax, Tmin):
        super().__init__(input_dim, output_dim, slide_window)
        self.ET_net = ET_net
        self.Q_net = Q_net
        self.f = f
        self.Smax = Smax
        self.Qmax = Qmax
        self.Df = Df
        self.Tmax = Tmax
        self.Tmin = Tmin

        # inner model series
        self.Precp_series = None
        self.Temp_series = None
        self.Lday_series = None

        # means and stds
        self.means = None
        self.stds = None

    def refresh_series(self, batch_ode_input, means, stds):
        self.Precp_series = batch_ode_input[:, 0]
        self.Temp_series = batch_ode_input[:, 1]
        self.Lday_series = batch_ode_input[:, 2]
        self.means = means
        self.stds = stds

    def forward(self, t, S):
        S_snow, S_water = S[0], S[1]
        t = min(torch.floor(t).to(torch.int).item(), self.Precp_series.shape[0] - 1)
        t = max(0, t)
        Precp, Temp, Lday = self.Precp_series[t], self.Temp_series[t], self.Lday_series[t]
        # 归一化处理
        S_snow_norm = (S_snow - self.means[0]) / self.stds[0]
        S_water_norm = (S_water - self.means[1]) / self.stds[1]
        Precp_norm = (Precp - self.means[2]) / self.stds[2]
        Temp_norm = (Temp - self.means[3]) / self.stds[3]

        ET_output = self.ET_net(torch.tensor([S_snow_norm, S_water_norm, Temp_norm]).unsqueeze(0))
        Q_output = self.Q_net(torch.tensor([S_water_norm, Precp_norm]).unsqueeze(0))
        melt_output = M(S_snow, Temp, self.Df, self.Tmax)
        dS_1 = Ps(Precp, Temp, self.Tmin) - melt_output
        dS_2 = Pr(Precp, Temp, self.Tmin) + melt_output - step_fct(S_water) * Lday * torch.exp(ET_output) - step_fct(
            S_water) * torch.exp(Q_output)
        return dS_1, dS_2


class M50_ODEFunc2(BaseTorchModel):
    def __init__(self, input_dim, output_dim, slide_window, ET_net, Q_net, f, Smax, Qmax, Df, Tmax, Tmin):
        super().__init__(input_dim, output_dim, slide_window)
        self.ET_net = ET_net
        self.Q_net = Q_net
        self.f = f
        self.Smax = Smax
        self.Qmax = Qmax
        self.Df = Df
        self.Tmax = Tmax
        self.Tmin = Tmin

        # means and stds
        self.means = None
        self.stds = None

    def refresh_series(self, batch_ode_input, means, stds):
        self.Precp = batch_ode_input[0]
        self.Temp = batch_ode_input[1]
        self.Lday = batch_ode_input[2]
        self.means = means
        self.stds = stds

    def forward(self, t, S):
        S_snow, S_water = S[0], S[1]
        Precp, Temp, Lday = self.Precp, self.Temp, self.Lday
        # 归一化处理
        S_snow_norm = (S_snow - self.means[0]) / self.stds[0]
        S_water_norm = (S_water - self.means[1]) / self.stds[1]
        Precp_norm = (Precp - self.means[2]) / self.stds[2]
        Temp_norm = (Temp - self.means[3]) / self.stds[3]

        ET_output = self.ET_net(torch.tensor([S_snow_norm, S_water_norm, Temp_norm]).unsqueeze(0))
        Q_output = self.Q_net(torch.tensor([S_water_norm, Precp_norm]).unsqueeze(0))
        melt_output = M(S_snow, Temp, self.Df, self.Tmax)
        dS_1 = Ps(Precp, Temp, self.Tmin) - melt_output
        dS_2 = Pr(Precp, Temp, self.Tmin) + melt_output - step_fct(S_water) * Lday * torch.exp(ET_output) - step_fct(
            S_water) * torch.exp(Q_output)
        return dS_1, dS_2


class M50(TorchLearner):
    def __init__(self, model: M50_ODEFunc, loss_metric, eval_metric_list):
        super().__init__(model, loss_metric, eval_metric_list)
        self.model = model
        self.factor_std = None
        self.factor_mean = None
        self.read_norm_info()

    def read_norm_info(self):
        import pandas as pd
        output = pd.read_csv(r'data/exp_hydro_output.csv')
        self.factor_std = torch.from_numpy(output.std().values.astype(np.float32))
        self.factor_mean = torch.from_numpy(output.mean().values.astype(np.float32))

    def predict_step(self, batch: Any, batch_idx: int, dataloader_idx: int = 0) -> Any:
        batch_x, batch_ode_input, batch_y = batch
        y0 = batch_x[0, 0] * self.factor_std[0] + self.factor_mean[0], \
             batch_x[0, 1] * self.factor_std[1] + self.factor_mean[1]
        batch_t = torch.linspace(0, batch_x.shape[0] - 1, steps=batch_x.shape[0]).to(torch.device('cpu'))
        # 统一输入
        self.model.refresh_series(batch_ode_input, self.factor_mean, self.factor_std)
        sol = odeint(self.model, y0=y0, t=batch_t, rtol=1e-3, atol=1e-3, adjoint_options=dict(norm='seminorm'))
        sol_1 = (sol[1].unsqueeze(1) - self.factor_mean[1]) / self.factor_std[1]
        # 一步一步求解
        # sol_list = []
        # for i in range(batch_x.shape[0]):
        #     self.model.refresh_series([batch_ode_input[i, 0], batch_ode_input[i, 1], batch_ode_input[i, 2]],
        #                               self.factor_mean, self.factor_std)
        #     temp_sol = odeint(self.model, y0=y0, t=torch.tensor([0, 1],dtype=torch.float32), rtol=1e-3, atol=1e-3)
        #     sol_list.append(torch.tensor([temp_sol[0][1],temp_sol[1][1]]).unsqueeze(0))
        #     y0 = (temp_sol[0][1], temp_sol[1][1])
        # sol_list = torch.concat(sol_list, dim=0)
        # sol_1 = (sol_list[:, 1].unsqueeze(1) - self.factor_mean[1]) / self.factor_std[1]
        y_out = torch.exp(self.model.Q_net(
            torch.concat([sol_1, batch_x[:, 2].unsqueeze(1)], dim=1))).unsqueeze(1)
        return batch_y, y_out


class M100_NN(BaseTorchModel):
    model_params = [SearchParam(name='hidden_units', dtype='int', low=16, high=32, step=8, default=32)]

    def __init__(self, input_dim, output_dim, slide_window, hidden_units=32):
        super(M100_NN, self).__init__(input_dim, output_dim, slide_window)
        self.model = nn.Sequential(nn.Linear(in_features=input_dim, out_features=hidden_units),
                                   nn.Tanh(),
                                   nn.Linear(in_features=hidden_units, out_features=hidden_units),
                                   nn.LeakyReLU(),
                                   nn.Linear(in_features=hidden_units, out_features=hidden_units),
                                   nn.LeakyReLU(),
                                   nn.Linear(in_features=hidden_units, out_features=hidden_units),
                                   nn.LeakyReLU(),
                                   nn.Linear(in_features=hidden_units, out_features=hidden_units),
                                   nn.LeakyReLU(),
                                   nn.Linear(in_features=hidden_units, out_features=output_dim))

    def forward(self, x):
        x = self.model(x).squeeze()
        return x


class M100_ODEFunc(BaseTorchModel):
    def __init__(self, input_dim, output_dim, slide_window, net, f, Smax, Qmax, Df, Tmax, Tmin):
        super().__init__(input_dim, output_dim, slide_window)
        self.net = net
        self.f = f
        self.Smax = Smax
        self.Qmax = Qmax
        self.Df = Df
        self.Tmax = Tmax
        self.Tmin = Tmin
        # inner model series
        self.Precp_series = None
        self.Temp_series = None
        self.Lday_series = None

        # means and stds
        self.means = None
        self.stds = None

    def refresh_series(self, batch_ode_input, means, stds):
        self.Precp_series = batch_ode_input[:, 0]
        self.Temp_series = batch_ode_input[:, 1]
        self.Lday_series = batch_ode_input[:, 2]
        self.means = means
        self.stds = stds

    def forward(self, t, S):
        S_snow, S_water = S[0], S[1]
        t = min(torch.floor(t).to(torch.int).item(), self.Precp_series.shape[0] - 1)
        t = max(0, t)

        Precp, Temp, Lday = self.Precp_series[t], self.Temp_series[t], self.Lday_series[t]
        S_snow_norm = (S_snow - self.means[0]) / self.stds[0]
        S_water_norm = (S_water - self.means[1]) / self.stds[1]
        Precp_norm = (Precp - self.means[2]) / self.stds[2]
        Temp_norm = (Temp - self.means[3]) / self.stds[3]

        net_output = self.net(torch.tensor([S_snow_norm, S_water_norm, Precp_norm, Temp_norm]).unsqueeze(0))
        melt_output = torch.relu(step_fct(S_snow)) * torch.sinh(net_output[2])
        dS_1 = torch.relu(torch.sinh(net_output[3]) * step_fct(-Temp)) - melt_output
        dS_2 = torch.relu(torch.sinh(net_output[4])) + melt_output - step_fct(
            S_water) * Lday * torch.exp(net_output[0]) - step_fct(S_water) * torch.exp(net_output[1])
        return dS_1, dS_2


class M100(TorchLearner):
    def __init__(self, model: nn.Module, loss_metric, eval_metric_list):
        super().__init__(model, loss_metric, eval_metric_list)
        self.model = model

        self.factor_std = None
        self.factor_mean = None
        self.read_norm_info()

    def read_norm_info(self):
        import pandas as pd
        output = pd.read_csv(r'data/exp_hydro_output.csv')
        self.factor_std = torch.from_numpy(output.std().values.astype(np.float32))
        self.factor_mean = torch.from_numpy(output.mean().values.astype(np.float32))

    def predict_step(self, batch: Any, batch_idx: int, dataloader_idx: int = 0) -> Any:
        batch_x, batch_ode_input, batch_y = batch
        y0 = batch_x[0, 0] * self.factor_std[0] + self.factor_mean[0], \
             batch_x[0, 1] * self.factor_std[1] + self.factor_mean[1]
        batch_t = torch.linspace(0, batch_x.shape[0] - 1, steps=batch_x.shape[0]).to(torch.device('cpu'))
        self.model.refresh_series(batch_ode_input, self.factor_mean, self.factor_std)
        sol = odeint(self.model, y0=y0, t=batch_t, rtol=1e-3, atol=1e-3)

        sol_0 = (sol[0].unsqueeze(1) - self.factor_mean[0]) / self.factor_std[0]
        sol_1 = (sol[1].unsqueeze(1) - self.factor_mean[1]) / self.factor_std[1]
        y_out = torch.exp(self.model.net(torch.concat([sol_0, sol_1, batch_x[:, 2].unsqueeze(1),
                                                       batch_x[:, 3].unsqueeze(1)], dim=1)))[:, 1].unsqueeze(1)
        return y_out, batch_y
