import torch.nn as nn

from hydroforecast.models.base_layers import noop


class ExplainRNNBase(nn.Module):
    def __init__(self, c_in, c_out, hidden_size=100, n_layers=1, bias=True, rnn_dropout=0, bidirectional=False, fc_dropout=0.):
        super().__init__()
        self.rnn = self._cell(c_in, hidden_size, num_layers=n_layers, bias=bias, batch_first=True, dropout=rnn_dropout,
                              bidirectional=bidirectional)
        self.dropout = nn.Dropout(fc_dropout) if fc_dropout else noop
        self.fc = nn.Linear(hidden_size * (1 + bidirectional), c_out)
        self.reset_parameters()

    def reset_parameters(self):
        for name, weight in self.named_parameters():
            if "bias" in name:
                weight.data.zero_()
            elif "weight" in name:
                nn.init.xavier_normal_(weight)
            # elif "weight_ih" in name:
            #     nn.init.normal_(weight, 0, 0.01)
            else:
                weight.data.normal_(0, 0.01)

    def forward_with_hidden(self, x, hidden=None):
        # 解释RNN模型，需要额外提供hidden反馈
        # modified by jingxin, the input is already [batch_size x seq_len x n_vars]
        # x = x.transpose(2,1)    # [batch_size x n_vars x seq_len] --> [batch_size x seq_len x n_vars]
        if self.is_reshape:
            x = self.flatten(x)
            x = x.unsqueeze(1)
        output, hidden = self.rnn(x, hidden)  # output from all sequence steps: [batch_size x seq_len x hidden_size * (1 + bidirectional)]
        output = output[:, -1]  # output from last sequence step : [batch_size x hidden_size * (1 + bidirectional)]
        output = self.fc(self.dropout(output))
        return output, hidden

    def forward(self, x, hidden=None):
        # 不返回hidden
        # 解释RNN模型，需要额外提供hidden反馈
        # modified by jingxin, the input is already [batch_size x seq_len x n_vars]
        # x = x.transpose(2,1)    # [batch_size x n_vars x seq_len] --> [batch_size x seq_len x n_vars]
        if self.is_reshape:
            x = self.flatten(x)
            x = x.unsqueeze(1)
        output, hidden = self.rnn(x, hidden)  # output from all sequence steps: [batch_size x seq_len x hidden_size * (1 + bidirectional)]
        output = output[:, -1]  # output from last sequence step : [batch_size x hidden_size * (1 + bidirectional)]
        output = self.fc(self.dropout(output))
        return output


class ExplainRNN(ExplainRNNBase):
    _cell = nn.RNN


class ExplainLSTM(ExplainRNNBase):
    _cell = nn.LSTM


class ExplainGRU(ExplainRNNBase):
    _cell = nn.GRU
