import tensorflow as tf
from hydroforecast.models import BaseModel


class BaseKerasModel(BaseModel, tf.keras.models.Model):
    model_params = []

    def __init__(self, input_dim, output_dim, slide_window):
        super().__init__(input_dim, output_dim, slide_window)

    def __str__(self):
        return 'Base keras model'

    @classmethod
    def build_model(cls, params):
        for param in cls.model_params:
            if param.name not in params.keys():
                params[param.name] = param.default
        return cls(**params)

    def call(self, inputs, training=None, mask=None):
        pass
