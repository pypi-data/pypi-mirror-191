import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from torchmetrics import MeanSquaredError, MeanAbsoluteError
from hydroforecast.exp.exp_path import ExpPath
from hydroforecast.exp.torch_exp import TorchExp
from hydroforecast.loader.base_module import TorchDataModule
from hydroforecast.models.torch_models.torch_metric import nash_sutcliffe_efficiency
from hydroforecast.proj_test.expHydro.nn_models import M100, M100_NN, M100_ODEFunc, ODEFuncDataset, PretrainDataset

# load data
M100_df = pd.read_csv(r'data/pretrain_dataset(M100).csv')

# model pretrain
pretrain_module = TorchDataModule(M100_df, time_idx=None,
                                  feature_cols=['S_snow', 'S_water', 'Precp', 'Temp'],
                                  target_cols=['ET_mech', 'Q_mech', 'M_mech', 'Ps_mech', 'Pr_mech'],
                                  feature_scaler=StandardScaler(), target_scaler=None,
                                  dataset=PretrainDataset(slide_window=1, lead_time=0))
pretrain_exp_path = ExpPath(proj_path=r'/hydroforecast/proj_test/expHydro',
                            proj_nm='pretrain', model_nm='m100', seed=42)
pretrain_exp = TorchExp(exp_path=pretrain_exp_path, model_obj=M100_NN, max_epochs=100,
                        loss_metric=MeanSquaredError(),
                        eval_metric_list=[MeanAbsoluteError(), nash_sutcliffe_efficiency()])
pretrain_net = pretrain_exp.train(params={}, train_val_datamodule=pretrain_module, train_idx=0)
pretrain_real_arr, pretrain_pred_arr = pretrain_exp.forecast(pretrain_module, return_real=True)

# M50 model train
exp_output_df = pd.read_csv(r'data/exp_hydro_output.csv')
means = exp_output_df[['precp', 'temp', 'Lday']].mean()
stds = exp_output_df[['precp', 'temp', 'Lday']].std()

exp_target_df = pd.read_csv(r'data/flow_target.csv')
train_df = pd.concat([exp_output_df, exp_target_df], axis=1)
m100_train_module = TorchDataModule(train_df, time_idx=None,
                                    feature_scaler=StandardScaler(), target_scaler=None, shuffle=False,
                                    batch_size=64,
                                    feature_cols=['S_snow', 'S_water', 'precp', 'temp', 'Lday'], target_cols=['flow'],
                                    dataset=ODEFuncDataset(slide_window=1, lead_time=0, means=means, stds=stds))
m100_exp_path = ExpPath(proj_path=r'/hydroforecast/proj_test/expHydro',
                        proj_nm='train', model_nm='m100', seed=42)
m100_exp = TorchExp(exp_path=m100_exp_path, model_obj=M100_ODEFunc, max_epochs=100, exp_learner=M100,
                    loss_metric=MeanSquaredError(), eval_metric_list=[nash_sutcliffe_efficiency()])

# main train
m100_pretrain_net = m100_exp.train(params={'net': pretrain_net,
                                           'f': 0.017, 'Smax': 1709.46, 'Qmax': 18.47,
                                           'Df': 2.67, 'Tmax': 0.176, 'Tmin': -2.09},
                                   train_val_datamodule=m100_train_module, train_idx=0)

real_arr, pred_arr = m100_exp.forecast(m100_train_module, return_real=True)
plt.plot(real_arr)
plt.plot(pred_arr)
plt.show()
result_df = pd.DataFrame({'real': real_arr.squeeze().tolist(), 'pred': pred_arr.squeeze().tolist()})
result_df.to_csv('M100_pred_result.csv', index=False)
