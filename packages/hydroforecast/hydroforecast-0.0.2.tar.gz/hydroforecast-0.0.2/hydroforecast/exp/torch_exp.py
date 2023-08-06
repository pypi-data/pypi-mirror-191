import os
import numpy as np
import torch
import torch.nn as nn
import pytorch_lightning as pl

from typing import List
from pytorch_lightning.accelerators import CPUAccelerator, CUDAAccelerator
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint, TQDMProgressBar
from optuna.integration.pytorch_lightning import PyTorchLightningPruningCallback
from sklearn.metrics import mean_squared_error
from torchmetrics import Metric

from hydroforecast.exp.base_exp import BaseExp
from hydroforecast.exp.exp_path import ExpPath
from hydroforecast.loader.base_module import TorchDataModule
from hydroforecast.optimization.optuna_search import OptunaHyperSearch


class TorchLearner(pl.LightningModule):
    def __init__(self, model: nn.Module,
                 loss_metric: Metric, eval_metric_list: List[Metric],
                 save_state=True):
        super(TorchLearner, self).__init__()
        self.model = model
        self.save_state = save_state

        self.train_loss_metric = loss_metric
        self.val_loss_metric = loss_metric
        self.train_eval_metric_list = eval_metric_list
        self.val_eval_metric_list = eval_metric_list

    def training_step(self, batch, batch_idx):
        y, y_hat = self.predict_step(batch, batch_idx)
        for metric_idx, log_metric in enumerate(self.train_eval_metric_list):
            self.log('train_metric_' + str(metric_idx + 1), log_metric(y, y_hat), prog_bar=True, on_step=True,
                     on_epoch=False)
        train_loss = self.train_loss_metric(y, y_hat)
        self.log('train_loss', train_loss, prog_bar=True, on_step=True, on_epoch=False)
        return train_loss

    def validation_step(self, batch, batch_idx):
        y, y_hat = self.predict_step(batch, batch_idx)
        for metric_idx, log_metric in enumerate(self.val_eval_metric_list):
            self.log('val_metric_' + str(metric_idx + 1), log_metric(y, y_hat),
                     prog_bar=True, on_step=True, on_epoch=True)
        val_loss = self.val_loss_metric(y, y_hat)
        self.log('val_loss', val_loss, prog_bar=True, on_step=True, on_epoch=True)
        return val_loss

    def predict_step(self, batch, batch_idx: int, dataloader_idx: int = 0):
        x, y = batch
        x = x.to(self.device)
        y = y.to(self.device).squeeze(1)
        y_hat = self.model.forward(x)
        return y, y_hat

    def test_step(self, batch, batch_idx):
        if self.save_state:
            # todo 路径设置
            torch.save(self.model, 'save.pt')
        return self.validation_step(batch, batch_idx)

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=0.01, weight_decay=1e-3)
        return {"optimizer": optimizer,
                "lr_scheduler": torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)}


class TorchExp(BaseExp):
    EXP_NAME = 'Pytorch EXP'
    MODEL_NAME = 'Pytorch family'
    MODEL_PARAMS = []

    def __init__(self, exp_path: ExpPath, model_obj,
                 max_epochs: int = 100, exp_learner=TorchLearner,
                 loss_metric=None, eval_metric_list=None, search_metric=mean_squared_error,
                 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
        super(TorchExp, self).__init__(exp_path)
        self.model_obj = model_obj
        self.max_epochs = max_epochs
        self.exp_learner = exp_learner
        self.loss_metric = loss_metric
        self.eval_metric_list = eval_metric_list
        self.search_metric = search_metric
        self.device = device

        self.best_hyperparams: dict = {}
        self.best_learner = None
        self.best_model = None

    def build_model(self, params, datamodule):
        params['input_dim'] = len(datamodule.feature_cols)
        params['output_dim'] = len(datamodule.target_cols)
        params['slide_window'] = datamodule.dataset.slide_window
        return self.model_obj.build_model(params).to(self.device)

    def get_save_path(self, search_idx):
        best_trial_path = os.path.join(self.exp_path.checkpoint_path, 'tune_history', 'trial_{}'.format(search_idx))
        model_states_name = os.listdir(best_trial_path)
        best_states = np.argmin(
            np.array([float(nm.split('-')[1].split('=')[1].split('.ckpt')[0]) for nm in model_states_name]))

        return os.path.join(best_trial_path, model_states_name[best_states])

    def get_trainer(self, callbacks=None):
        trainer = pl.Trainer(
            max_epochs=self.max_epochs,
            gradient_clip_val=1,
            accelerator=CUDAAccelerator() if torch.cuda.is_available() else CPUAccelerator(),
            enable_checkpointing=True,
            logger=False,
            default_root_dir=os.path.join(self.exp_path.checkpoint_path, 'tune_history'),
            callbacks=callbacks
        )
        return trainer

    def get_callbacks(self, temp_check_point_path, optuna_trial=None):
        es = EarlyStopping(monitor="val_loss", mode="min", patience=5)
        mc = ModelCheckpoint(dirpath=temp_check_point_path, save_last=False,
                             monitor="val_loss", mode="min", save_top_k=1,
                             filename='{epoch}-{val_loss:.4f}')
        bar = TQDMProgressBar(refresh_rate=1)
        callbacks = [es, mc, bar]
        if optuna_trial:
            callbacks.append([PyTorchLightningPruningCallback(optuna_trial, monitor='val_loss')])
        return [es, mc, bar]

    def train(self, params, train_val_datamodule: TorchDataModule, train_idx=0):
        temp_checkpoint_path = os.path.join(self.exp_path.checkpoint_path, 'train_history',
                                            'train_{}'.format(train_idx))
        model = self.build_model(params=params, datamodule=train_val_datamodule)
        file_path = os.path.join(temp_checkpoint_path, 'model_state.pt')
        if os.path.exists(file_path):
            file_path = os.path.join(temp_checkpoint_path, 'model_state.pt')
            model.load_state_dict(torch.load(file_path))
            self.best_learner = self.exp_learner(model, self.loss_metric, self.eval_metric_list)
        else:
            self.best_learner = self.exp_learner(model, self.loss_metric, self.eval_metric_list)
            train_dataloader, val_dataloader = train_val_datamodule.get_sample()
            trainer = self.get_trainer(self.get_callbacks(temp_checkpoint_path))
            trainer.fit(self.best_learner, train_dataloaders=train_dataloader, val_dataloaders=val_dataloader)
            torch.save(self.best_learner.model.state_dict(), os.path.join(temp_checkpoint_path, 'model_state.pt'))
        self.best_model = model
        return model

    def calibrate(self, search_method: OptunaHyperSearch, train_val_datamodule: TorchDataModule):
        best_search_idx, self.best_hyperparams = search_method.optimal(self, train_val_datamodule, self.MODEL_PARAMS)
        temp_args = {'model': self.build_model(params=self.best_hyperparams, datamodule=train_val_datamodule),
                     'eval_metric': self.loss_metric,
                     'log_metric_list': self.eval_metric_list}
        best_learner = self.exp_learner(**temp_args).load_from_checkpoint(
            self.get_save_path(best_search_idx), **temp_args)
        self.best_learner = best_learner
        self.best_model = best_learner.model

    def evaluate(self, params, train_val_datamodule: TorchDataModule, search_idx: int, optuna_trial=None):
        model = self.build_model(params=params, datamodule=train_val_datamodule)
        learner = self.exp_learner(model, self.loss_metric, self.eval_metric_list)
        train_dataloader, val_dataloader = train_val_datamodule.get_sample()
        temp_checkpoint_path = os.path.join(self.exp_path.checkpoint_path, 'tune_history',
                                            'trial_{}'.format(search_idx))
        trainer = self.get_trainer(self.get_callbacks(temp_checkpoint_path, optuna_trial))
        trainer.fit(learner, train_dataloaders=train_dataloader, val_dataloaders=val_dataloader)
        predict_result = trainer.predict(learner, dataloaders=val_dataloader)
        val_real, val_predict = self.handle_predict(predict_result)
        return self.search_metric(val_real, val_predict)

    def forecast(self, datamodule: TorchDataModule, return_real=False):
        trainer = self.get_trainer(callbacks=[])
        datamodule.datamodule_type = 'test'
        dataloader = datamodule.get_sample()
        real_arr, pred_arr = self.handle_predict(trainer.predict(self.best_learner, dataloaders=dataloader))
        if datamodule.target_scaler is not None:
            real_arr = datamodule.target_scaler.inverse_transform(real_arr)
            pred_arr = datamodule.target_scaler.inverse_transform(pred_arr)
        return real_arr, pred_arr

    @staticmethod
    def handle_predict(result):
        real_list = []
        pred_list = []
        for r in result:
            pred, real = r
            real_list.append(real.cpu().detach().numpy())
            pred_list.append(pred.cpu().detach().numpy())
        real_arr = np.concatenate(real_list, axis=0)
        pred_arr = np.concatenate(pred_list, axis=0)
        return real_arr, pred_arr
