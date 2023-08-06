from typing import List, Union
import pandas as pd
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from torch.utils.data import DataLoader as TDataLoader
from torch.utils.data import random_split
from paddle.io import DataLoader as PDataLoader


class BaseDataModule(object):
    def __init__(self, data: pd.DataFrame, time_idx: str, feature_cols: List[str], target_cols: Union[List[str], str],
                 feature_scaler=StandardScaler(), target_scaler=StandardScaler(), datamodule_type='train'):
        self.data = data
        self.time_idx = time_idx
        self.time_series = data.pop(time_idx) if time_idx is not None else None
        self.feature_cols = feature_cols
        self.target_cols = target_cols if isinstance(target_cols, List) else [target_cols]
        self.feature_scaler = feature_scaler
        self.target_scaler = target_scaler
        self.datamodule_type = datamodule_type
        self.scaled_feature, self.scaled_target = None, None
        self.normalize()

    def normalize(self):
        if self.datamodule_type == 'train':
            if self.feature_scaler is not None:
                self.scaled_feature = self.feature_scaler.fit_transform(self.data[self.feature_cols])
            else:
                self.scaled_feature = self.data[self.feature_cols].values
            if self.target_scaler is not None:
                self.scaled_target = self.target_scaler.fit_transform(self.data[self.target_cols])
            else:
                self.scaled_target = self.data[self.target_cols].values
        elif self.datamodule_type in ['test', 'val']:
            if self.feature_scaler is not None:
                self.scaled_feature = self.feature_scaler.transform(self.data[self.feature_cols])
            else:
                self.scaled_feature = self.data[self.feature_cols].values
            if self.target_scaler is not None:
                self.scaled_target = self.target_scaler.transform(self.data[self.target_cols])
            else:
                self.scaled_target = self.data[self.target_cols].values
        else:
            raise NotImplementedError

    def get_attributes(self):
        kwargs = {'time_idx': self.time_idx, 'feature_cols': self.feature_cols, 'target_cols': self.target_cols,
                  'feature_scaler': self.feature_scaler, 'target_scaler': self.target_scaler}
        return kwargs

    @classmethod
    def from_datamodule(cls, data, datamodule, datamodule_type='test'):
        kwargs = datamodule.get_attributes()
        kwargs['datamodule_type'] = datamodule_type
        return cls(data, **kwargs)

    def get_sample(self):
        pass


class TorchDataModule(BaseDataModule):
    def __init__(self, data: pd.DataFrame, time_idx: Union[str, None], feature_cols: List[str], target_cols: List[str],
                 feature_scaler=StandardScaler(), target_scaler=StandardScaler(), datamodule_type='train',
                 batch_size: int = 64, shuffle: bool = True, dataset=None,
                 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'), num_workers: int = 0):
        # load exp config
        super().__init__(data, time_idx, feature_cols, target_cols, feature_scaler, target_scaler, datamodule_type)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.dataset = dataset
        self.device = device
        self.num_workers = num_workers
        self.normalize()

    def get_sample(self):

        if self.datamodule_type == 'train':
            if self.shuffle:
                dataset = self.dataset.set_data(self.scaled_feature, self.scaled_target, self.dataset)
                train_dataset, val_dataset = random_split(
                    dataset=dataset,
                    lengths=[int(len(dataset) * 0.8), len(dataset) - int(len(dataset) * 0.8)],
                    generator=torch.Generator().manual_seed(42))
            else:
                train_dataset = self.dataset.set_data(self.scaled_feature[:int(len(self.scaled_feature) * 0.8), :],
                                                      self.scaled_target[:int(len(self.scaled_feature) * 0.8), :],
                                                      self.dataset)
                val_dataset = self.dataset.set_data(self.scaled_feature[:int(len(self.scaled_feature) * 0.8), :],
                                                    self.scaled_target[:int(len(self.scaled_feature) * 0.8), :],
                                                    self.dataset)
            return TDataLoader(train_dataset, shuffle=False, batch_size=self.batch_size, num_workers=self.num_workers), \
                TDataLoader(val_dataset, shuffle=False, batch_size=self.batch_size, num_workers=self.num_workers)
        elif self.datamodule_type == 'test':
            dataset = self.dataset.set_data(self.scaled_feature, self.scaled_target, self.dataset)
            return TDataLoader(dataset, shuffle=False, batch_size=self.batch_size, num_workers=self.num_workers)


class PaddleDataModule(BaseDataModule):
    def __init__(self, data: pd.DataFrame, time_idx: Union[str, None], feature_cols: List[str], target_cols: List[str],
                 feature_scaler=StandardScaler(), target_scaler=StandardScaler(), datamodule_type='train',
                 batch_size: int = 64, shuffle: bool = True, dataset=None,
                 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'), num_workers: int = 0):
        # load exp config
        super().__init__(data, time_idx, feature_cols, target_cols, feature_scaler, target_scaler, datamodule_type)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.dataset = dataset
        self.device = device
        self.num_workers = num_workers
        self.normalize()

    def get_sample(self):

        if self.datamodule_type == 'train':
            if self.shuffle:
                dataset = self.dataset.set_data(self.scaled_feature, self.scaled_target, self.dataset)
                train_dataset, val_dataset = random_split(
                    dataset=dataset,
                    lengths=[int(len(dataset) * 0.8), len(dataset) - int(len(dataset) * 0.8)],
                    generator=torch.Generator().manual_seed(42))
            else:
                train_dataset = self.dataset.set_data(self.scaled_feature[:int(len(self.scaled_feature) * 0.8), :],
                                                      self.scaled_target[:int(len(self.scaled_feature) * 0.8), :],
                                                      self.dataset)
                val_dataset = self.dataset.set_data(self.scaled_feature[:int(len(self.scaled_feature) * 0.8), :],
                                                    self.scaled_target[:int(len(self.scaled_feature) * 0.8), :],
                                                    self.dataset)
            return PDataLoader(train_dataset, shuffle=False, batch_size=self.batch_size, num_workers=self.num_workers), \
                PDataLoader(val_dataset, shuffle=False, batch_size=self.batch_size, num_workers=self.num_workers)
        elif self.datamodule_type == 'test':
            dataset = self.dataset.set_data(self.scaled_feature, self.scaled_target, self.dataset)
            return PDataLoader(dataset, shuffle=False, batch_size=self.batch_size, num_workers=self.num_workers)


class NumpyDataModule(BaseDataModule):
    def __init__(self, data: pd.DataFrame, time_idx: str, feature_cols: List[str], target_cols: List[str],
                 feature_scaler=StandardScaler(), target_scaler=StandardScaler(), datamodule_type='train',
                 slide_window: int = 10, lead_time: int = 1, shuffle: bool = True):
        # load exp config
        super().__init__(data, time_idx, feature_cols, target_cols, feature_scaler, target_scaler, datamodule_type)
        self.slide_window = slide_window
        self.lead_time = lead_time
        self.shuffle = shuffle

    def get_sample(self):

        def sample_slide(feature, target):
            sample = np.array([feature[i:i + self.slide_window, :].reshape(1, -1) for i in
                               range(len(feature) - self.slide_window - self.lead_time + 1)]).squeeze()
            target = target[self.slide_window:, ]
            return sample, target

        x, y = sample_slide(self.scaled_feature, self.scaled_target)
        if self.datamodule_type == 'train':
            train_x, val_x, train_y, val_y = train_test_split(x, y, test_size=0.2, shuffle=self.shuffle,
                                                              random_state=42)
            return train_x, val_x, train_y, val_y
        elif self.datamodule_type == 'proj_test':
            return x, y


class HydroDataModule(object):
    def __init__(self, data: pd.DataFrame, time_idx: str, climate_cols: List[str], streamflow_col: str = None):
        self.data = data
        self.time_idx = time_idx
        self.time_series = data.pop(time_idx)
        self.climate_cols = climate_cols
        self.streamflow_col = streamflow_col
        self.climate_data = self.data[climate_cols]
        self.streamflow_obs = self.data[streamflow_col] if streamflow_col else None

    def get_attributes(self):
        kwargs = {'time_idx': self.time_idx, 'climate_cols': self.climate_cols, 'streamflow_col': self.streamflow_col}
        return kwargs

    @classmethod
    def from_datamodule(cls, data, datamodule, streamflow_col=None):
        kwargs = datamodule.get_attributes()
        if not streamflow_col:
            kwargs['streamflow_col'] = None
        return cls(data, **kwargs)

    def get_sample(self):
        if self.streamflow_col:
            return self.climate_data.values, self.streamflow_obs.values
        else:
            return self.climate_data.values
