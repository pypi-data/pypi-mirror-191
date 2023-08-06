import os

import joblib
import paddle
import numpy as np
from paddle.hapi.callbacks import EarlyStopping, LRScheduler, ModelCheckpoint, ProgBarLogger

from hydroforecast.optimization.optuna_search import OptunaHyperSearch

from hydroforecast.exp.exp_path import ExpPath
from hydroforecast.exp.base_exp import BaseExp
from hydroforecast.loader.base_module import PaddleDataModule


class BasePaddleWrapper(object):
    def __init__(self, model, epochs, loss_metric, eval_metric):
        self.model = model
        self.epochs = epochs
        self.loss_metric = loss_metric
        self.eval_metric = eval_metric

        self.optim = None

    def train(self, train_dataloader):
        if not self.optim:
            self.configure_optimizers()
        self.model.train()
        for epoch in range(self.epochs):
            for batch_id, data in enumerate(train_dataloader):
                x, y = data[0], data[1]
                y_hat = self.model(x)
                loss_metric = self.loss_metric(y, y_hat)
                eval_metric = self.eval_metric(y, y_hat)
                loss_metric.backward()
                if (batch_id + 1) % 900 == 0:
                    print("epoch: {}, batch_id: {}, loss is: {}, acc is: {}".format(
                        epoch, batch_id + 1, loss_metric.numpy(), eval_metric.numpy()))
                self.optim.step()
                self.optim.clear_grad()

    def evaluate(self, val_dataloader):
        self.model.eval()
        loss_list = []
        for batch_id, data in enumerate(val_dataloader()):
            x, y = data[0], data[1]
            y_hat = self.model(x)
            # 计算损失与精度
            loss_metric = self.loss_metric(y_hat, y)
            eval_metric = self.eval_metric(y_hat, y)

            # 打印信息
            if (batch_id + 1) % 30 == 0:
                print("batch_id: {}, loss is: {}, acc is: {}".format(
                    batch_id + 1, loss_metric.numpy(), eval_metric.numpy()))
            loss_list.append(loss_metric)
        return paddle.mean(loss_list)

    def predict(self, test_datamodule):
        self.model.eval()
        real_list, pred_list = [], []
        for batch_id, data in enumerate(test_datamodule()):
            x, y = data[0], data[1]
            y_hat = self.model(x)
            real_list.append(y.numpy()[np.newaxis, :])
            pred_list.append(y_hat.numpy()[np.newaxis, :])
        real_arr = np.concatenate(real_list, axis=0)
        pred_arr = np.concatenate(pred_list, axis=0)
        return real_arr, pred_arr

    def configure_optimizers(self, optim):
        self.optim = paddle.optimizer.AdamW(parameters=self.model.parameters(), learning_rate=0.01, weight_decay=1e-3)


class PaddleExp(BaseExp):
    TRAINER_NAME = 'Paddle EXP'
    TRAINER_MODEL = 'Paddle family'

    def __init__(self, exp_path: ExpPath, model_obj, loss_metric, eval_metric_list, max_epochs):
        super(PaddleExp, self).__init__(exp_path)
        self.model_obj = model_obj
        self.loss_metric = loss_metric
        self.eval_metric_list = eval_metric_list
        self.max_epochs = max_epochs

        self.best_hyperparams: dict = {}
        self.best_model = None

    def build_model(self, params, datamodule):
        params['input_dim'] = len(datamodule.feature_cols)
        params['output_dim'] = len(datamodule.target_cols)
        params['slide_window'] = datamodule.dataset.slide_window
        return self.model_obj.build_model(params)

    def callbacks(self, temp_check_point_path, optuna_trial=None):
        es = EarlyStopping('loss', mode='auto', patience=5)
        mc = ModelCheckpoint(save_freq=10, save_dir=temp_check_point_path)
        ls = LRScheduler()
        pb = ProgBarLogger(verbose=1, log_freq=10)
        return [es, mc, ls, pb]

    def optim(self, model, lr):
        return paddle.optimizer.Adam(learning_rate=lr, parameters=model.parameters())

    def calibrate(self, search_method: OptunaHyperSearch, train_val_datamodule: PaddleDataModule):
        best_search_idx, self.best_hyperparams = search_method.optimal(self, train_val_datamodule, self.MODEL_PARAMS)
        model = self.build_model(self.best_hyperparams, train_val_datamodule)
        train_x, val_x, train_y, val_y = train_val_datamodule.get_sample()
        model.fit(train_x, train_y)
        save_path = os.path.join(self.exp_path.checkpoint_path, 'tune_history')
        joblib.dump(model, save_path)
        self.best_model = model

    def evaluate(self, params, train_val_datamodule: PaddleDataModule, search_idx: int, optuna_trial=None):
        model = self.build_model(params=params, datamodule=train_val_datamodule)
        train_dataloader, val_dataloader = train_val_datamodule.get_sample()
        temp_checkpoint_path = os.path.join(self.exp_path.checkpoint_path,
                                            'tune_history', 'trial_{}'.format(search_idx))
        model_wrapper = self._train(model, train_val_datamodule, temp_checkpoint_path)
        eval_result = model_wrapper.evaluate(eval_data=val_dataloader, batch_size=train_val_datamodule.batch_size)
        return eval_result

    def _train(self, model, train_val_datamodule, temp_checkpoint_path):
        model_wrapper = paddle.Model(model)
        train_dataloader, val_dataloader = train_val_datamodule.get_sample()
        model_wrapper.prepare(optimizer=self.optim(model, lr=1e-2),
                              loss=self.loss_metric,
                              metrics=self.eval_metric_list)
        model_wrapper.fit(train_data=train_dataloader, eval_data=val_dataloader, epochs=self.max_epochs,
                          batch_size=train_val_datamodule.batch_size,
                          save_dir=temp_checkpoint_path, callbacks=self.callbacks(temp_checkpoint_path))
        return model_wrapper

    def train(self, params, train_val_datamodule: PaddleDataModule, train_idx=0):
        temp_checkpoint_path = os.path.join(self.exp_path.checkpoint_path, 'train_history',
                                            'train_{}'.format(train_idx))
        file_path = os.path.join(temp_checkpoint_path, 'best_model.pdparams')
        self.best_model = self.build_model(params=params, datamodule=train_val_datamodule)
        if os.path.exists(file_path):
            file_path = os.path.join(temp_checkpoint_path, 'best_model.pdparams')
            self.best_model.set_state_dict(paddle.load(file_path))
        else:
            model_wrapper: paddle.Model = self._train(self.best_model, train_val_datamodule, temp_checkpoint_path)
            paddle.save(model_wrapper.network.state_dict(),
                        os.path.join(temp_checkpoint_path, 'best_model.pdparams'))
            self.best_model = model_wrapper.network
        return self.best_model

    def forecast(self, datamodule: PaddleDataModule, return_real=False):
        datamodule.datamodule_type = 'test'
        temp_dataloader = datamodule.get_sample()
        model_wrapper = paddle.Model(network=self.best_model)
        model_wrapper.prepare(
            optimizer=self.optim(self.best_model, lr=1e-2),
            loss=self.loss_metric, metrics=self.eval_metric_list)
        pred_batches = model_wrapper.predict(temp_dataloader, batch_size=datamodule.batch_size)[0]
        pred_arr = np.concatenate(pred_batches)
        real_arr = temp_dataloader.dataset.target
        if datamodule.target_scaler is not None:
            pred_arr = datamodule.target_scaler.inverse_transform(pred_arr.reshape(-1, 1))
            real_arr = datamodule.target_scaler.inverse_transform(real_arr.reshape(-1, 1))
        return real_arr, pred_arr
