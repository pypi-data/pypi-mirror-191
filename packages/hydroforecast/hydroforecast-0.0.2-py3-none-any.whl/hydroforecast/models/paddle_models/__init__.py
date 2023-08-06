import paddle.nn as nn
from hydroforecast.models import BaseModel


class BasePaddleModel(BaseModel, nn.Layer):
    model_params = []

    def __init__(self, input_dim, output_dim, slide_window):
        BaseModel.__init__(self, input_dim, output_dim, slide_window)
        nn.Layer.__init__(self)

    def __str__(self):
        return 'Base Paddle model'

    @classmethod
    def build_model(cls, params):
        for param in cls.model_params:
            if param.name not in params.keys():
                params[param.name] = param.default
        return cls(**params)
