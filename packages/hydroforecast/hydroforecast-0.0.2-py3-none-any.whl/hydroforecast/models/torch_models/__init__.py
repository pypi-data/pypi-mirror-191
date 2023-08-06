import torch
import torch.nn as nn

from hydroforecast.models import BaseModel



class BaseTorchModel(BaseModel, nn.Module):
    model_params = []

    def __init__(self, input_dim, output_dim, slide_window,
                 device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')):
        BaseModel.__init__(self, input_dim, output_dim, slide_window)
        nn.Module.__init__(self)
        self.device = device

    def __str__(self):
        return 'Base torch model'

    def init_parameters(self):
        for name, weight in self.named_parameters():
            if "bias" in name:
                weight.data.zero_()
            elif "weight" in name:
                nn.init.xavier_normal_(weight)
            else:
                weight.data.normal_(0, 0.01)

    @classmethod
    def build_model(cls, params):
        for param in cls.model_params:
            if param.name not in params.keys():
                params[param.name] = param.default
        return cls(**params)
