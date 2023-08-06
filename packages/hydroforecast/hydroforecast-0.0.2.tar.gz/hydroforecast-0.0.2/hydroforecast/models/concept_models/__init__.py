from typing import List
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from hydroforecast.optimization import SearchParam


class SimResult(object):
    def __init__(self, name, info=None):
        self.name = name
        self.info = info
        self.value = None

    def init_value(self, time_len):
        self.value = np.zeros(shape=(time_len,))

    def set_value(self, value, time_idx):
        self.value[time_idx] = value


class HydroModel(object):
    stores_series: List[SimResult]
    fluxes_series: List[SimResult]
    model_params: List[SearchParam]
    uhs = ()
    error_series = SimResult('error')

    def __init__(self, param_values, delta_t=1):
        self.param_values = param_values
        self.delta_t = delta_t
        self.status = False

    @classmethod
    def build_model(cls, param_values, delta_t=1):
        return cls(param_values, delta_t)

    @staticmethod
    def model_func(t, S, param_values, uhs, climate_inter, delta_t, return_fluxes=False):
        raise NotImplementedError

    def solve(self, s_old, climate_iter):
        if len(climate_iter) == 1:
            P, Ep, T = climate_iter[0], 0, 0
        elif len(climate_iter) == 2:
            P, Ep, T = climate_iter[0], climate_iter[1], 0
        elif len(climate_iter) == 3:
            P, Ep, T = climate_iter[0], climate_iter[1], climate_iter[2]
        else:
            raise NotImplementedError
        func_args = (self.param_values, self.uhs, (P, Ep, T), self.delta_t)
        res = solve_ivp(self.model_func, y0=s_old, t_span=(0, 1),
                        t_eval=[1], method='RK45', rtol=1e-8, atol=1e-8, args=func_args)
        s_new = res.y
        func_args = func_args + (True,)
        delta_s, fluxes = self.model_func(1, s_old, *func_args)
        error = np.sum(s_new) - np.sum(s_old) - np.sum(np.array(delta_s))
        return s_new, fluxes, error

    def run(self, input_climate, stores_old, simulate_results: tuple = None):
        time_len = input_climate.shape[0]
        if simulate_results:
            temp_stores_series, temp_fluxes_series, temp_error_series = simulate_results
        else:
            temp_stores_series, temp_fluxes_series, temp_error_series = self.stores_series, self.fluxes_series, self.error_series
        temp_stores_series = self.init_simulation_result(temp_stores_series, time_len + 1)
        temp_fluxes_series = self.init_simulation_result(temp_fluxes_series, time_len)
        temp_error_series.init_value(time_len)
        for time_idx in range(time_len):
            stores_new, fluxes, error = self.solve(s_old=stores_old, climate_iter=input_climate[time_idx, :])
            temp_stores_series = self.update_simulation(temp_stores_series, stores_old, time_idx)
            temp_fluxes_series = self.update_simulation(temp_fluxes_series, fluxes, time_idx)
            temp_error_series.set_value(error, time_idx)
            stores_old = stores_new.squeeze().tolist()
            self.step(fluxes)
        temp_stores_series = self.update_simulation(temp_stores_series, stores_old, time_len)
        if simulate_results:
            return temp_stores_series, temp_fluxes_series, temp_error_series
        else:
            self.status = True
            self.stores_series, self.fluxes_series, self.error_series = temp_stores_series, temp_fluxes_series, temp_error_series

    def step(self, *args, **kwargs):
        pass

    def forecast(self, input_climate, stores_old=None, return_all=False):
        if not self.status:
            raise RuntimeError("please run model first")
        stores_old = stores_old if stores_old else [ss.value[-1] for ss in self.stores_series]
        simulate_results = (self.stores_series, self.fluxes_series, self.error_series)
        temp_stores_series, temp_fluxes_series, temp_error_series = self.run(input_climate, stores_old,
                                                                             simulate_results)
        if return_all:
            return self.parse_simulation_result(temp_stores_series, temp_fluxes_series)
        else:
            q_series = np.sum([f.value for f in temp_fluxes_series if f.info == 'Streamflow'], axis=0)
            return pd.DataFrame(q_series, columns=['Streamflow'])

    def get_streamflow(self, input_climate, S0):
        if not self.status:
            self.run(input_climate, S0)
        q_flux = [f.value for f in self.fluxes_series if f.info == 'Streamflow']
        return pd.DataFrame(np.sum(q_flux, 0), columns=['Streamflow'])

    def get_all_output(self, input_climate, S0):
        if not self.status:
            self.run(input_climate, S0)
        output_flux_series, all_flux_series, all_store_series = self.parse_simulation_result(self.stores_series,
                                                                                             self.fluxes_series)
        return output_flux_series, all_flux_series, all_store_series

    @staticmethod
    def parse_simulation_result(stores_series, fluxes_series):
        e_series = np.sum([f.value for f in fluxes_series if f.info == 'Evaporation'], axis=1)
        q_series = np.sum([f.value for f in fluxes_series if f.info == 'Streamflow'], axis=1)
        output_flux_series = pd.DataFrame({'Evaporation': e_series, 'Streamflow': q_series})
        all_flux_series = pd.DataFrame({f.name: f.value for f in fluxes_series})
        all_store_series = pd.DataFrame({store.name: store.value for store in stores_series})
        return output_flux_series, all_flux_series, all_store_series

    @staticmethod
    def init_simulation_result(simulation_result, time_len):
        for sr in simulation_result:
            sr.init_value(time_len=time_len)
        return simulation_result

    @staticmethod
    def update_simulation(simulation_result, temp_list: List, time_idx):
        for i, sr in enumerate(temp_list):
            simulation_result[i].set_value(sr, time_idx)
        return simulation_result
