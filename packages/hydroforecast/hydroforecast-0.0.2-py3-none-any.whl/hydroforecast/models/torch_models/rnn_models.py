import torch.nn as nn
from hydroforecast.models.torch_models import BaseTorchModel
from hydroforecast.optimization import SearchParam


# Cell
class BaseRNN(BaseTorchModel):
    MODEL_PARAMS = [SearchParam(name='n_layers', dtype='int', low=1, high=2, step=1, default=1),
                    SearchParam(name='hidden_size', dtype='int', low=16, high=256, step=16, default=64),
                    SearchParam(name='fc_dropout', dtype='float', low=0.0, high=0.2, step=0.02, default=0.0),
                    SearchParam(name='rnn_dropout', dtype='float', low=0.0, high=0.2, step=0.02, default=0.0)]
    rnn_cell = None

    def __init__(self, input_dim, output_dim, slide_window,
                 hidden_size=100, n_layers=1, bias=True, rnn_dropout=0.,
                 bidirectional=False, fc_dropout=0.):
        super().__init__(input_dim, output_dim, slide_window)
        self.rnn = self.rnn_cell(input_dim, hidden_size, num_layers=n_layers, bias=bias, batch_first=True,
                                 dropout=rnn_dropout, bidirectional=bidirectional)
        self.dropout = nn.Dropout(fc_dropout) if fc_dropout else lambda x: x
        self.fc = nn.Linear(hidden_size * (1 + bidirectional), output_dim)
        self.init_parameters()

    def __str__(self):
        raise NotImplementedError

    def forward(self, x):
        output, _ = self.rnn(x)
        output = output[:, -1]
        output = self.fc(self.dropout(output))
        return output


class RNN(BaseRNN):
    rnn_cell = nn.RNN

    def __str__(self):
        return 'RNN'


class LSTM(BaseRNN):
    rnn_cell = nn.LSTM

    def __str__(self):
        return 'LSTM'


class GRU(BaseRNN):
    rnn_cell = nn.GRU

    def __str__(self):
        return 'GRU'
