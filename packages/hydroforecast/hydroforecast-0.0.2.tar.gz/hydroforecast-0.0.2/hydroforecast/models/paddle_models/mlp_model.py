import paddle.nn as nn

from hydroforecast.models.paddle_models import BasePaddleModel


class Reshape(nn.Layer):
    def __init__(self, *shape):
        super(Reshape, self).__init__()
        self.shape = shape

    def forward(self, x):
        return x.reshape(x.shape[0], *self.shape)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(['bs'] + [str(s) for s in self.shape])})"


# Cell
class MLP(BasePaddleModel):
    def __init__(self, input_dim, output_dim, slide_window, hidden_size=128, n_layers=1, p=0.):
        super().__init__(input_dim, output_dim, slide_window)
        self.flatten = Reshape(-1)
        self.mlp = nn.Sequential(
            nn.Linear(input_dim * slide_window, hidden_size),
            nn.Dropout(p=p),
            nn.ReLU()
        )
        self.head = nn.Linear(hidden_size, output_dim)

    def forward(self, x):
        x = self.flatten(x)
        x = self.mlp(x)
        return self.head(x)
