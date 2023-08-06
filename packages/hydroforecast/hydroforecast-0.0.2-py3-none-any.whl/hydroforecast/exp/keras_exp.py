import os

import joblib
from sklearn.model_selection import KFold

from build.lib.hydroforecast.optimization.optuna_search import OptunaHyperSearch
from hydroforecast.exp.exp_path import ExpPath

from keras import layers, regularizers, models, callbacks, optimizers
import numpy as np
from keras.models import clone_model
from optuna.integration import KerasPruningCallback
from hydroforecast.exp.base_exp import BaseExp
from hydroforecast.loader.base_module import NumpyDataModule

os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # cpu环境


class KerasExp(BaseExp):
    TRAINER_NAME = 'Keras EXP'
    TRAINER_MODEL = 'Keras family'

    def __init__(self, exp_path: ExpPath, model_obj, loss_metric, eval_metric_list, max_epochs, batch_size,
                 cross_validate: bool = True):
        super(KerasExp, self).__init__(exp_path)
        self.model_obj = model_obj
        self.loss_metric = loss_metric
        self.eval_metric_list = eval_metric_list
        self.cross_validate = cross_validate
        self.max_epochs = max_epochs
        self.batch_size = batch_size

        self.best_hyperparams: dict = {}
        self.best_model = None

    def build_model(self, params, datamodule):
        params['input_dim'] = len(datamodule.feature_cols)
        params['output_dim'] = len(datamodule.target_cols)
        params['slide_window'] = datamodule.slide_window
        return self.model_obj.build_model(params)

    def get_callbacks(self, temp_check_point_path, optuna_trial=None):
        es = callbacks.EarlyStopping(monitor='val_mse', mode='min', verbose=1, patience=10,
                                     min_delta=0.01, restore_best_weights=True)
        reduce = callbacks.ReduceLROnPlateau(monitor='val_mse', factor=0.5, patience=5, verbose=1,
                                             mode='min', min_delta=0.01, cooldown=0, min_lr=1e-2 / 100)
        tnan = callbacks.TerminateOnNaN()
        mc = callbacks.ModelCheckpoint(filepath=temp_check_point_path, verbose=1, monitor='val_loss',
                                       save_best_only=False)
        callbacks_list = [es, reduce, mc, tnan]
        if optuna_trial is not None:
            prune = KerasPruningCallback(optuna_trial, monitor='val_loss')
            callbacks_list.append([prune])
        return callbacks_list

    def calibrate(self, search_method: OptunaHyperSearch, train_val_datamodule: NumpyDataModule):
        best_search_idx, self.best_hyperparams = search_method.optimal(self, train_val_datamodule, self.MODEL_PARAMS)
        model = self.build_model(self.best_hyperparams, train_val_datamodule)
        train_x, val_x, train_y, val_y = train_val_datamodule.get_sample()
        temp_checkpoint_path = os.path.join(self.exp_path.checkpoint_path, 'tune_history', 'best')
        model = self._fit(model, train_x=train_x, train_y=train_y, callbacks=self.get_callbacks(temp_checkpoint_path))
        save_path = os.path.join(self.exp_path.checkpoint_path, 'tune_history')
        joblib.dump(model, save_path)
        self.best_model = model

    def train(self, params, train_val_datamodule: NumpyDataModule, search_idx: int, optuna_trial=None):
        model = self.build_model(params, train_val_datamodule)
        train_x, val_x, train_y, val_y = train_val_datamodule.get_sample()
        temp_checkpoint_path = os.path.join(self.exp_path.checkpoint_path, 'tune_history',
                                            'trial_{}'.format(search_idx))

        model = self._fit(model, train_x=train_x, train_y=train_y,
                          callbacks=self.get_callbacks(temp_checkpoint_path, optuna_trial))
        return model

    def evaluate(self, params, train_val_datamodule: NumpyDataModule, search_idx: int, optuna_trial=None):
        model = self.build_model(params, train_val_datamodule)
        train_x, val_x, train_y, val_y = train_val_datamodule.get_sample()
        temp_checkpoint_path = os.path.join(self.exp_path.checkpoint_path, 'tune_history',
                                            'trial_{}'.format(search_idx))
        if self.cross_validate:
            train_val_x = np.concatenate([train_x, val_x], axis=0)
            train_val_y = np.concatenate([train_y, val_y], axis=0)
            kf = KFold(n_splits=5)
            eval_list = []
            step_idx = 0
            for train_index, test_index in kf.split(train_val_x, train_val_y):
                model_copy = clone_model(model)
                train_predictor, train_target = train_val_x[train_index], train_val_y[train_index]
                val_predictor, val_target = train_val_x[test_index], train_val_y[test_index]
                model_copy = self._fit(model_copy, train_x=train_predictor, train_y=train_target,
                                       callbacks=self.get_callbacks(temp_checkpoint_path, optuna_trial))
                val_pred = model_copy.predict(val_predictor)
                eval_mse = self.loss_metric(val_target, val_pred)
                eval_list.append(eval_mse)
                step_idx = step_idx + 1
            return np.mean(eval_list)
        else:
            model = self._fit(model, train_x=train_x, train_y=train_y,
                              callbacks=self.get_callbacks(temp_checkpoint_path, optuna_trial))
            pred_y = model.predict(val_x)
            eval_result = self.loss_metric(val_y, pred_y)
            return eval_result

    def _fit(self, model, train_x, train_y, val_x=None, val_y=None, callbacks=None):
        model.compile(loss=self.loss_metric, metrics=self.eval_metric_list, optimizer=optimizers.Adam(lr=1e-2))
        model.fit(train_x, train_y, validation_data=(val_x, val_y), callbacks=callbacks, epochs=self.max_epochs,
                  batch_size=self.batch_size)
        return model

    def forecast(self, datamodule: NumpyDataModule, return_real=False):
        x, y = datamodule.get_sample()
        pred_y = self.best_model.predict(x)
        real_arr_inv = datamodule.target_scaler.inverse_transform(y.reshape(-1, 1))
        pred_arr_inv = datamodule.target_scaler.inverse_transform(pred_y.reshape(-1, 1))
        return real_arr_inv, pred_arr_inv
