# reference from https://github.com/locuslab/TCN
import torch.nn as nn
from torch.nn.utils import weight_norm

from hydroforecast.models.torch_models import BaseTorchModel
from hydroforecast.optimization import SearchParam


class Chomp1d(nn.Module):
    """
    Args:
        remove padding
    """

    def __init__(self, chomp_size):
        super(Chomp1d, self).__init__()
        self.chomp_size = chomp_size

    def forward(self, x):
        return x[:, :, :-self.chomp_size].contiguous()


class TemporalBlock(nn.Module):
    def __init__(self, n_inputs, n_outputs, kernel_size, stride, dilation, padding, dropout=0.2):
        super(TemporalBlock, self).__init__()
        self.conv1 = weight_norm(nn.Conv1d(n_inputs, n_outputs, kernel_size,
                                           stride=stride, padding=padding, dilation=dilation))
        self.chomp1 = Chomp1d(padding)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(dropout)

        self.conv2 = weight_norm(nn.Conv1d(n_outputs, n_outputs, kernel_size,
                                           stride=stride, padding=padding, dilation=dilation))
        self.chomp2 = Chomp1d(padding)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(dropout)

        self.net = nn.Sequential(self.conv1, self.chomp1, self.relu1, self.dropout1,
                                 self.conv2, self.chomp2, self.relu2, self.dropout2)
        self.downsample = nn.Conv1d(n_inputs, n_outputs, 1) if n_inputs != n_outputs else None
        self.relu = nn.ReLU()
        self.init_weights()

    def init_weights(self):
        self.conv1.weight.data.normal_(0, 0.01)
        self.conv2.weight.data.normal_(0, 0.01)
        if self.downsample is not None:
            self.downsample.weight.data.normal_(0, 0.01)

    def forward(self, x):
        out = self.net(x)
        res = x if self.downsample is None else self.downsample(x)
        return self.relu(out + res)


class TCN(BaseTorchModel):
    MODEL_PARAMS = [SearchParam(name='n_layers', dtype='int', low=1, high=2, step=1, default=1),
                    SearchParam(name='hidden_size', dtype='int', low=16, high=256, step=16, default=64),
                    SearchParam(name='dropout', dtype='float', low=0.0, high=0.2, step=0.02, default=0.0)]

    def __init__(self, input_dim, output_dim, slide_window, hidden_size, n_layers, dropout):
        super(TCN, self).__init__(input_dim, output_dim, slide_window)
        num_channels = [hidden_size] * n_layers
        kernel_size = 2
        layers = []
        num_levels = len(num_channels)
        for i in range(num_levels):
            dilation_size = 2 ** i
            in_channels = input_dim if i == 0 else num_channels[i - 1]
            out_channels = num_channels[i]
            # one temporalBlock can be seen from fig1(b).
            layers += [TemporalBlock(in_channels, out_channels, kernel_size, stride=1, dilation=dilation_size,
                                     padding=(kernel_size - 1) * dilation_size, dropout=dropout)]

        self.network = nn.Sequential(*layers)
        self.out_proj = nn.Linear(hidden_size, output_dim)

    def forward(self, x):
        """
            x: batch_size, seq_len, input_dim
        """
        x = x.transpose(1, 2)
        out = self.network(x)[:, :, -1:]  # 最后一步
        out = self.out_proj(out.transpose(1, 2))
        return out
