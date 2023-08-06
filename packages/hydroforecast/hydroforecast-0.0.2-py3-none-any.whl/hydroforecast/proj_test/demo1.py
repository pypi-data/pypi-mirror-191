import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from hydroforecast.exp.exp_path import ExpPath
from exp.hyper_search import OptunaHyperSearch
from hydroforecast.exp.torch_exp import GRUExp
from hydroforecast.loader.base_module import TorchDataModule
from torchmetrics.regression import MeanAbsoluteError, MeanSquaredError, MeanAbsolutePercentageError

test_df = pd.read_csv(r'/data/test_data.csv')
train_val_module = TorchDataModule(test_df.iloc[:10000, ], time_idx='date',
                                   feature_cols=test_df.columns[1:], target_cols=[test_df.columns[-1]],
                                   slide_window=10, lead_time=1)
test_module = train_val_module.from_datamodule(test_df.iloc[10000:, ], train_val_module)
exp_path = ExpPath(proj_path=r'/', proj_nm='demo1', model_nm='xgb', seed=42)
search_method = OptunaHyperSearch(direction='minimize', n_trial=5, path=exp_path, seed=42)
exp = GRUExp(exp_path, max_epochs=100, loss_metric=MeanSquaredError(), eval_metric_list=[MeanAbsoluteError(),MeanAbsolutePercentageError()],
             search_metric=mean_squared_error)
exp.calibrate(search_method, train_val_module)
real_arr_inv, pred_arr_inv = exp.forecast(train_val_module)
r2_score(real_arr_inv, pred_arr_inv)
