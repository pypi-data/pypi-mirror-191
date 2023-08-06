import torch.nn as nn


class Reshape(nn.Module):
    def __init__(self, *shape):
        super(Reshape, self).__init__()
        self.shape = shape

    def forward(self, x):
        return x.reshape(x.shape[0], *self.shape)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(['bs'] + [str(s) for s in self.shape])})"


# Cell
class MLP(nn.Module):
    def __init__(self, c_in, c_out, slide_window, layers=None, ps=None):
        super(MLP, self).__init__()
        if len(ps) <= 1:
            ps = ps * len(layers)
        assert len(layers) == len(ps), '#layers and #ps must match'
        self.flatten = Reshape(-1)
        nf = [c_in * slide_window] + layers
        self.mlp = nn.ModuleList()
        for i in range(len(layers)):
            self.mlp.append(nn.Linear(nf[i], nf[i + 1]))
            self.mlp.append(nn.Dropout(ps[i]))
            self.mlp.append(nn.ReLU())
        _head = [nn.Linear(nf[-1], c_out)]
        self.head = nn.Sequential(*_head)

    def forward(self, x):
        x = self.flatten(x)
        for mlp in self.mlp:
            x = mlp(x)
        return self.head(x)
