class BaseModel(object):
    model_params = []

    def __init__(self, input_dim, output_dim, slide_window):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.slide_window = slide_window

    def __str__(self):
        raise NotImplementedError

    @classmethod
    def build_model(cls, params):
        for param in cls.model_params:
            if param.name not in params.keys():
                params[param.name] = param.default
        return cls(**params)
