import numpy as np
import paddle
import paddle.nn as nn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from hydroforecast.exp.exp_path import ExpPath
from hydroforecast.exp.paddle_exp import PaddleExp
from hydroforecast.loader.base_dataset import PaddleDataset
from hydroforecast.loader.base_module import PaddleDataModule
from hydroforecast.models.paddle_models import BasePaddleModel
from hydroforecast.optimization import SearchParam


class TempNet(BasePaddleModel):
    model_params = [SearchParam(name='hidden_units', dtype='int', low=16, high=32, step=8, default=16)]

    def __init__(self, input_dim, output_dim, slide_window, hidden_units=16):
        super(TempNet, self).__init__(input_dim, output_dim, slide_window)
        self.model = nn.Sequential(nn.Linear(in_features=input_dim, out_features=hidden_units),
                                   nn.Tanh(),
                                   nn.Linear(in_features=hidden_units, out_features=hidden_units),
                                   nn.LeakyReLU(),
                                   nn.Linear(in_features=hidden_units, out_features=output_dim))

    def forward(self, x):
        x = self.model(x)
        return x


class TempDataset(PaddleDataset):
    def __len__(self):
        return len(self.feature)

    def __getitem__(self, i):
        if i >= len(self):
            return ValueError()
        x = paddle.to_tensor(self.feature[i, :].astype(np.float32))
        y = paddle.to_tensor(self.target[i, :].astype(np.float32))
        return x, y


# load data
ET_df = pd.read_csv(r'../expHydro/data/pretrain_dataset(ET).csv')

# ET model pretrain
train_module = PaddleDataModule(ET_df, time_idx=None, feature_cols=['S_snow', 'S_water', 'Temp'], target_cols=['ET'],
                                feature_scaler=StandardScaler(), target_scaler=None,
                                dataset=TempDataset(slide_window=1, lead_time=0))
exp_path = ExpPath(proj_path=r'/hydroforecast/proj_test/paddle_test',
                   proj_nm='pretrain', model_nm='et', seed=42)
temp_exp = PaddleExp(exp_path=exp_path, model_obj=TempNet, max_epochs=100,
                     loss_metric=paddle.nn.MSELoss(),
                     eval_metric_list=None)
train_net = temp_exp.train(params={}, train_val_datamodule=train_module, train_idx=2)
real_arr, pred_arr = temp_exp.forecast(train_module, return_real=True)
plt.plot(real_arr)
plt.plot(pred_arr)
plt.show()
