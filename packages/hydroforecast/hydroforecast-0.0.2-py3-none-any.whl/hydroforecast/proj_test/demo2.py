import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import scipy.io as scio

from hydroforecast.exp.exp_path import ExpPath
from hydroforecast.exp.hydrology_exp import HydrologyExp
from hydroforecast.loader.base_module import HydroDataModule
from hydroforecast.models.concept_models.hymod import HYMOD
from hydroforecast.optimization.spotpy_search import SpotpySearch

data = scio.loadmat(r'F:\pycharm\My Project\My Lib\Conceptual_Model\example\data\MARRMoT_example_data.mat')
precip = data['data_MARRMoT_examples']['precipitation'][0][0].squeeze().tolist()
temp = data['data_MARRMoT_examples']['temperature'][0][0].squeeze().tolist()
pet = data['data_MARRMoT_examples']['potential_evapotranspiration'][0][0].squeeze().tolist()
streamflow = data['data_MARRMoT_examples']['streamflow'][0][0].squeeze().tolist()
temp_df = pd.DataFrame({'precip': precip, 'temp': temp, 'pet': pet, 'streamflow': streamflow})
temp_df['date'] = pd.date_range('19900101', periods=len(temp_df), freq='d')
train_val_module = HydroDataModule(temp_df.iloc[800:1000, ], time_idx='date', climate_cols=['precip', 'pet', 'temp'], streamflow_col='streamflow')
test_module = train_val_module.from_datamodule(temp_df.iloc[1000:, ], train_val_module)

exp_path = ExpPath(proj_path=r'/', proj_nm='demo2', model_nm='hymod', seed=42)
search_method = SpotpySearch(direction='minimize', n_trial=100, path=exp_path, seed=42)
exp = HydrologyExp(exp_path, model_obj=HYMOD, eval_metric=mean_squared_error, store_init=(15, 7, 3, 8, 22))
exp.calibrate(search_method, train_val_module)
pred_arr_inv = exp.forecast(test_module)
r2_score(temp_df['streamflow'][1000:].values, pred_arr_inv.values)

import matplotlib.pyplot as plt
plt.plot(pred_arr_inv.values)
plt.plot(temp_df['streamflow'][1000:].values)
plt.show()