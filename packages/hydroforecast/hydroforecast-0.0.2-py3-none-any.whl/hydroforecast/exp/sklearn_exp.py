import os

import joblib
import numpy as np
from sklearn.model_selection import KFold

from build.lib.hydroforecast.optimization.optuna_search import OptunaHyperSearch
from hydroforecast.exp.base_exp import BaseExp
from hydroforecast.exp.exp_path import ExpPath
from hydroforecast.loader.base_module import NumpyDataModule


class SklearnExp(BaseExp):
    TRAINER_NAME = 'Sklearn EXP'
    TRAINER_MODEL = 'Sklearn family'
    MODEL_PARAMS = []

    def __init__(self, exp_path: ExpPath, model_obj, eval_metric, cross_validate: bool = True):
        super(SklearnExp, self).__init__(exp_path)
        self.model_obj = model_obj
        self.eval_metric = eval_metric
        self.cross_validate = cross_validate

        self.best_hyperparams: dict = {}
        self.best_model = None

    def build_model(self, params, datamodule):
        params['input_dim'] = len(datamodule.feature_cols)
        params['output_dim'] = len(datamodule.target_cols)
        params['slide_window'] = datamodule.slide_window
        return self.model_obj.build_model(params)

    def train(self, params, train_val_datamodule: NumpyDataModule, train_idx=0):
        model_wrapper = self.build_model(params, train_val_datamodule)
        train_x, val_x, train_y, val_y = train_val_datamodule.get_sample()
        temp_checkpoint_path = os.path.join(self.exp_path.checkpoint_path, 'train_history',
                                            'train_{}'.format(train_idx))
        if os.path.exists(temp_checkpoint_path):
            os.makedirs(temp_checkpoint_path)

        if os.path.exists(os.path.join(temp_checkpoint_path, 'model.m')):
            return model_wrapper.load_model(os.path.join(temp_checkpoint_path, 'model.m'))
        model_wrapper.fit_model(train_x=train_x, train_y=train_y)
        model_wrapper.save_model(temp_checkpoint_path)
        return model_wrapper.model

    def calibrate(self, search_method: OptunaHyperSearch, train_val_datamodule: NumpyDataModule):
        best_search_idx, self.best_hyperparams = search_method.optimal(self, train_val_datamodule, self.MODEL_PARAMS)
        model = self.build_model(self.best_hyperparams, train_val_datamodule)
        train_x, val_x, train_y, val_y = train_val_datamodule.get_sample()
        model.fit(train_x, train_y)
        save_path = os.path.join(self.exp_path.checkpoint_path, 'tune_history')
        joblib.dump(model, save_path)
        self.best_model = model

    def evaluate(self, params, train_val_datamodule: NumpyDataModule, search_idx: int, optuna_trial=None):
        model_wrapper = self.build_model(params, train_val_datamodule)
        train_x, val_x, train_y, val_y = train_val_datamodule.get_sample()
        if self.cross_validate:
            train_val_x = np.concatenate([train_x, val_x], axis=0)
            train_val_y = np.concatenate([train_y, val_y], axis=0)
            kf = KFold(n_splits=5)
            eval_list = []
            step_idx = 0
            for train_index, test_index in kf.split(train_val_x, train_val_y):
                model_wrapper_copy = self.build_model(params, train_val_datamodule)
                train_predictor, train_target = train_val_x[train_index], train_val_y[train_index]
                val_predictor, val_target = train_val_x[test_index], train_val_y[test_index]
                model_wrapper_copy.fit_model(train_x=train_predictor, train_y=train_target)
                val_pred = model_wrapper_copy.predict(val_predictor)
                eval_mse = self.eval_metric(val_target, val_pred)
                eval_list.append(eval_mse)
                step_idx = step_idx + 1
            return np.mean(eval_list)
        else:
            model_wrapper.fit_model(train_x=train_x, train_y=train_y)
            pred_y = model_wrapper.predict(val_x)
            eval_result = self.eval_metric(val_y, pred_y)
            return eval_result

    def forecast(self, datamodule: NumpyDataModule):
        x, y = datamodule.get_sample()
        pred_y = self.best_model.predict(x)
        if datamodule.target_scaler:
            real_arr = datamodule.target_scaler.inverse_transform(y.reshape(-1, 1))
            pred_arr = datamodule.target_scaler.inverse_transform(pred_y.reshape(-1, 1))
        else:
            real_arr = y.reshape(-1, 1)
            pred_arr = pred_y.reshape(-1, 1)
        return real_arr, pred_arr
