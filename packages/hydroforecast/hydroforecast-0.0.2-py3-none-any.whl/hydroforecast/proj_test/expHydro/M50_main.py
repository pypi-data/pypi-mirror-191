import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from torchmetrics import MeanSquaredError, MeanAbsoluteError

from hydroforecast.exp.exp_path import ExpPath
from hydroforecast.exp.torch_exp import TorchExp
from hydroforecast.loader.base_module import TorchDataModule
from hydroforecast.models.torch_models.torch_metric import nash_sutcliffe_efficiency
from hydroforecast.proj_test.expHydro.nn_models import M50_NN, M50, M50_ODEFunc, ODEFuncDataset, PretrainDataset

# load data
ET_df = pd.read_csv(r'data/pretrain_dataset(ET).csv')
Q_df = pd.read_csv(r'data/pretrain_dataset(Q).csv')

# ET model pretrain
ET_train_module = TorchDataModule(ET_df, time_idx=None, feature_cols=['S_snow', 'S_water', 'Temp'], target_cols=['ET'],
                                  feature_scaler=StandardScaler(), target_scaler=None,
                                  dataset=PretrainDataset(slide_window=1, lead_time=0))
et_exp_path = ExpPath(proj_path=r'/hydroforecast/proj_test/expHydro',
                      proj_nm='pretrain', model_nm='et', seed=42)
et_exp = TorchExp(exp_path=et_exp_path, model_obj=M50_NN, max_epochs=100,
                  loss_metric=MeanSquaredError(), eval_metric_list=[MeanAbsoluteError(), nash_sutcliffe_efficiency()])
et_pretrain_net = et_exp.train(params={}, train_val_datamodule=ET_train_module, train_idx=0)
et_real_arr, et_pred_arr = et_exp.forecast(ET_train_module, return_real=True)
plt.plot(et_real_arr)
plt.plot(et_pred_arr)
plt.show()
r2_score(et_real_arr, et_pred_arr)
# Q model pretrain
Q_train_module = TorchDataModule(Q_df, time_idx=None, feature_cols=['S_water', 'Precp'], target_cols=['Q'],
                                 feature_scaler=StandardScaler(), target_scaler=None,
                                 dataset=PretrainDataset(slide_window=1, lead_time=0))
q_exp_path = ExpPath(proj_path=r'/hydroforecast/proj_test/expHydro',
                     proj_nm='pretrain', model_nm='q', seed=42)
q_exp = TorchExp(exp_path=q_exp_path, model_obj=M50_NN, max_epochs=100,
                 loss_metric=MeanSquaredError(), eval_metric_list=[MeanAbsoluteError(), nash_sutcliffe_efficiency()])
Q_pretrain_net = q_exp.train(params={}, train_val_datamodule=Q_train_module, train_idx=0)
q_real_arr, q_pred_arr = q_exp.forecast(Q_train_module, return_real=True)
plt.plot(q_real_arr)
plt.plot(q_pred_arr)
plt.show()
r2_score(q_real_arr, q_pred_arr)

# M50 model train
exp_output_df = pd.read_csv(r'data/exp_hydro_output.csv')
means = exp_output_df[['precp', 'temp', 'Lday']].mean()
stds = exp_output_df[['precp', 'temp', 'Lday']].std()

exp_target_df = pd.read_csv(r'data/flow_target.csv')
train_df = pd.concat([exp_output_df, exp_target_df], axis=1)
m50_train_module = TorchDataModule(train_df, time_idx=None,
                                   feature_scaler=StandardScaler(), target_scaler=None, shuffle=False,
                                   batch_size=64,
                                   feature_cols=['S_snow', 'S_water', 'precp', 'temp', 'Lday'], target_cols=['flow'],
                                   dataset=ODEFuncDataset(slide_window=1, lead_time=0, means=means, stds=stds))
m50_exp_path = ExpPath(proj_path=r'/hydroforecast/proj_test/expHydro',
                       proj_nm='train', model_nm='m50', seed=22)
m50_exp = TorchExp(exp_path=m50_exp_path, model_obj=M50_ODEFunc, max_epochs=100, exp_learner=M50,
                   loss_metric=MeanSquaredError(), eval_metric_list=[nash_sutcliffe_efficiency()])

# main train
m50_pretrain_net = m50_exp.train(params={'ET_net': et_pretrain_net, 'Q_net': Q_pretrain_net,
                                         'f': 0.017, 'Smax': 1709.46, 'Qmax': 18.47,
                                         'Df': 2.67, 'Tmax': 0.176, 'Tmin': -2.09},
                                 train_val_datamodule=m50_train_module, train_idx=0)

real_arr, pred_arr = m50_exp.forecast(m50_train_module, return_real=True)
plt.plot(real_arr)
plt.plot(pred_arr)
plt.show()
r2_score(real_arr, pred_arr)
result_df = pd.DataFrame({'real': real_arr.squeeze().tolist(), 'pred': pred_arr.squeeze().tolist()})
result_df.to_csv('M50_pred_result.csv', index=False)
