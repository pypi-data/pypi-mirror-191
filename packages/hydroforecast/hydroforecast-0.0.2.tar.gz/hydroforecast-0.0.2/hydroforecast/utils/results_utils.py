import os
import numpy as np
import pandas as pd
import xarray as xr
import json
import matplotlib.pyplot as plt
from neuralhydrology.evaluation.metrics import get_available_metrics, calculate_metrics, mean_peak_timing


def analysis_forecast(self, real_array, pred_array, time_stamp, result_type, dataset_type):
    save_path = os.path.join(self.exp_path.save_path, result_type, dataset_type)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if len(pred_array.shape) > 1:
        pred_mean = np.median(pred_array, axis=1)
        pd.DataFrame(pred_array).to_csv(save_path + '\\' + 'preds.csv', index=False)
    else:
        pred_mean = pred_array
    pred_xr = xr.DataArray(pred_mean)
    real_xr = xr.DataArray(real_array)
    criteria = get_available_metrics()[:-1]
    metrics = calculate_metrics(real_xr, pred_xr, metrics=criteria)
    if time_stamp is not None:
        pred_xr_with_date = xr.DataArray(pred_mean, coords=[time_stamp.values], dims=['date'])
        real_xr_with_date = xr.DataArray(real_array, coords=[time_stamp.values], dims=['date'])
        metrics['Peak-Timing'] = mean_peak_timing(real_xr_with_date, pred_xr_with_date)
    with open(save_path + "\\criteria.json", "w") as f:
        f.write(json.dumps(metrics, ensure_ascii=False, indent=4, separators=(',', ':')))
    pd.DataFrame({'real': real_array, 'pred': pred_mean}).to_csv(save_path + '\\' + 'result.csv', index=False)
    plt.figure(figsize=(18, 5))
    plt.plot(real_array, linestyle='--')
    plt.plot(pred_mean, linestyle='--')
    plt.savefig(save_path + '\\' + 'line_plot.png')
    plt.close()