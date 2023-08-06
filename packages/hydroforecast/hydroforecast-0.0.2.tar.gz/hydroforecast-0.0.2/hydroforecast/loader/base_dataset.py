import torch
import paddle
import numpy as np
from torch.utils.data import Dataset as TDataset
from paddle.io import Dataset as PDataset


class TorchDataset(TDataset):
    slide_window = None
    lead_time = None
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    def __init__(self, slide_window, lead_time,
                 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'),
                 feature=None, target=None):
        # property
        self.slide_window = slide_window
        self.lead_time = lead_time
        self.device = device

        # data
        self.feature = feature
        self.target = target

    @classmethod
    def set_data(cls, feature, target, dataset):
        # required before training
        return cls(slide_window=dataset.slide_window, lead_time=dataset.lead_time, device=dataset.device,
                   feature=feature, target=target)

    def __len__(self):
        return len(self.feature) - self.slide_window - self.lead_time + 1

    def __getitem__(self, i):
        if i >= len(self):
            return ValueError()
        start = i
        s_end = i + self.slide_window
        r_end = s_end + self.lead_time

        x = torch.from_numpy(self.feature[start: s_end, :].astype(np.float32)).to(self.device)
        y = torch.from_numpy(self.target[r_end - 1: r_end, :].astype(np.float32)).to(self.device)
        return x, y


class PaddleDataset(PDataset):
    slide_window = None
    lead_time = None

    def __init__(self, slide_window, lead_time, feature=None, target=None):
        # property
        super().__init__()
        self.slide_window = slide_window
        self.lead_time = lead_time

        # data
        self.feature = feature
        self.target = target

    @classmethod
    def set_data(cls, feature, target, dataset):
        # required before training
        return cls(slide_window=dataset.slide_window, lead_time=dataset.lead_time, feature=feature, target=target)

    def __getitem__(self, idx):
        start = idx
        s_end = idx + self.slide_window
        r_end = s_end + self.lead_time

        x = paddle.to_tensor(self.feature[start: s_end, :].astype(np.float32))
        y = paddle.to_tensor(self.target[r_end - 1: r_end, :].astype(np.float32))
        return x, y

    def __len__(self):
        return len(self.feature) - self.slide_window - self.lead_time + 1
