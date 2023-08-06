import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from scipy.integrate import ode

data_path = r'E:\CAMELS\basin_dataset_public_v1p2'
basin_id = "01013500"
area = 2260093113
basin_huc = "01"
path_forcing_data = os.path.join(data_path, "basin_mean_forcing", "daymet", basin_huc,
                                 "{}_lump_cida_forcing_leap.txt".format(basin_id))
path_flow_data = os.path.join(data_path, "usgs_streamflow", basin_huc, "{}_streamflow_qc.txt".format(basin_id))
header = ['Date', 'dayl(s)', 'prcp(mm/day)', 'srad(W/m2)', 'swe(mm)', 'tmax(C)', 'tmin(C)', 'vp(Pa)']

forcing_df = pd.read_csv(path_forcing_data, skiprows=4, sep='\t', header=None)
raw_flow_df = pd.read_csv(path_flow_data, header=None)
forcing_df.columns = header
forcing_df['Date'] = pd.to_datetime(forcing_df['Date'])
flow_series = []
for flow in raw_flow_df.values:
    flow_series.append(np.float32(flow[0].split(' ')[-2]))
flow_series = np.array(flow_series)
flow_series[np.where(flow_series == -999)] = np.nan
flow_series = flow_series * (304.8 ** 3) / (area * 10 ** 6) * 86400
flow_df = pd.DataFrame(flow_series, columns=['flow'])
flow_df['Date'] = forcing_df['Date']
flow_df = flow_df[(flow_df['Date'] >= datetime(1980, 10, 1))
                  & (flow_df['Date'] <= datetime(2000, 9, 30))].drop('Date', axis=1)
forcing_df = forcing_df[(forcing_df['Date'] >= datetime(1980, 10, 1)) & (forcing_df['Date'] <= datetime(2000, 9, 30))]

precp_series = forcing_df.loc[:, 'prcp(mm/day)'].values
temp_series = forcing_df.loc[:, ['tmax(C)', 'tmin(C)']].values.mean(axis=1)
Lday_series = forcing_df.loc[:, 'dayl(s)'].values / 3600

S0 = [0.0, 1303.0042478479704]
param = (0.017, 1709.46, 18.47, 2.67, 0.176, -2.09)  # , 0.8137969540102923
step_fct = lambda x: (np.tanh(5.0 * x) + 1.0) * 0.5
Ps = lambda P, T, Tmin: step_fct(Tmin - T) * P
Pr = lambda P, T, Tmin: step_fct(T - Tmin) * P
M = lambda S0, T, Df, Tmax: step_fct(T - Tmax) * step_fct(S0) * np.minimum(S0, Df * (T - Tmax))
PET = lambda T, Lday: 29.8 * Lday * 0.611 * np.exp((17.3 * T) / (T + 237.3)) / (T + 273.2)
ET = lambda S1, T, Lday, Smax: step_fct(S1) * step_fct(S1 - Smax) * PET(T, Lday) + \
                               step_fct(S1) * step_fct(Smax - S1) * PET(T, Lday) * (S1 / Smax)
Qb = lambda S1, f, Smax, Qmax: step_fct(S1) * step_fct(S1 - Smax) * Qmax + step_fct(S1) * step_fct(
    Smax - S1) * Qmax * np.exp(-f * (Smax - S1))
Qs = lambda S1, Smax: step_fct(S1) * step_fct(S1 - Smax) * (S1 - Smax)


def exp_hydro(t, S, args):
    f, Smax, Qmax, Df, Tmax, Tmin = args
    S1, S2 = S
    t = int(t)
    precp = precp_series[t]
    temp = temp_series[t]
    Lday = Lday_series[t]
    Q_out = Qb(S2, f, Smax, Qmax) + Qs(S2, Smax)
    dS1 = Ps(precp, temp, Tmin) - M(S1, temp, Df, Tmax)
    dS2 = Pr(precp, temp, Tmin) + M(S1, temp, Df, Tmax) - ET(S2, temp, Lday, Smax) - Q_out
    return [dS1, dS2]


# 常微分方程计算
ode_solver = ode(f=exp_hydro).set_integrator('dopri5', rtol=1e-6, atol=1e-6)
ode_solver.set_initial_value(y=S0, t=0.).set_f_params(param)
total_t = len(precp_series) - 1
dt = 1
S_series = [np.array(S0)]
while ode_solver.t < total_t:
    S_t = ode_solver.integrate(ode_solver.t + dt)
    S_series.append(S_t)
S_series = np.array(S_series)
S_snow_series = S_series[:, 0]
S_water_series = S_series[:, 1]

# 后续内容补充
qb = Qb(S_water_series, 0.017, 1709.46, 18.47)
qs = Qs(S_water_series, 1709.46)

# 获取模型输入对象
result_df = pd.DataFrame({'S_snow': S_snow_series, 'S_water': S_water_series,
                          'precp': precp_series, 'temp': temp_series, 'Lday': Lday_series})
result_df.to_csv(r'data/exp_hydro_output.csv', index=False)
flow_df.to_csv(r'data/flow_target.csv', index=False)

# 准备预训练的数据
S_snow_bucket = result_df['S_snow'].values
S_water_bucket = result_df['S_water'].values
P_bucket = result_df['precp'].values
T_bucket = result_df['temp'].values
Lday_bucket = result_df['Lday'].values

f_bucket, Smax_bucket, Qmax_bucket, Df_bucket, Tmax_bucket, Tmin_bucket = 0.017, 1709.46, 18.47, 2.67, 0.176, -2.09
# evapotranspiration
ET_mech = ET(S_water_bucket, T_bucket, Lday_bucket, Smax_bucket)
ET_mech = np.array([x if x > 0.0 else 0.000000001 for x in ET_mech])
# melt
temp_T_mech = Df_bucket * (T_bucket - Tmax_bucket)
temp_T_mech = np.array([np.minimum(t, S0[1]) for t in temp_T_mech])
M_mech = temp_T_mech * step_fct(T_bucket - Tmax_bucket)
# discharge
Q_mech = Qb(S_water_bucket, f_bucket, Smax_bucket, Qmax_bucket) + Qs(S_water_bucket, Smax_bucket)
Q_mech = np.array([x if x > 0.0 else 0.000000001 for x in Q_mech])
plt.plot(np.log(Q_mech))
plt.show()
# snow precipitation
Ps_mech = Ps(P_bucket, T_bucket, Tmin_bucket)
# rain precipitation
Pr_mech = Pr(P_bucket, T_bucket, Tmin_bucket)

ET_df = pd.DataFrame(
    {'S_snow': S_snow_bucket, 'S_water': S_water_bucket, 'Temp': T_bucket, 'ET': np.log(ET_mech / Lday_bucket)})
Q_df = pd.DataFrame({'S_water': S_water_bucket, 'Precp': P_bucket, 'Q': np.log(Q_mech)})
ET_df.to_csv(r'data/pretrain_dataset(ET).csv', index=False)
Q_df.to_csv(r'data/pretrain_dataset(Q).csv', index=False)
M100_df = pd.DataFrame({'S_snow': S_snow_bucket, 'S_water': S_water_bucket, 'Precp': P_bucket, 'Temp': T_bucket,
                        'ET_mech': np.log(ET_mech / Lday_bucket), 'Q_mech': np.log(Q_mech),
                        'M_mech': np.arcsinh(M_mech), 'Ps_mech': np.arcsinh(Ps_mech), 'Pr_mech': np.arcsinh(Pr_mech)})
M100_df.to_csv(r'data/pretrain_dataset(M100).csv', index=False)
