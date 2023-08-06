from hydroforecast.models.keras_models import BaseKerasModel
from tensorflow import keras
from hydroforecast.optimization import SearchParam


class BaseRNN(BaseKerasModel):
    MODEL_PARAMS = [SearchParam(name='n_layers', dtype='int', low=1, high=2, step=1, default=1),
                    SearchParam(name='hidden_size', dtype='int', low=16, high=256, step=16, default=64),
                    SearchParam(name='fc_dropout', dtype='float', low=0.0, high=0.2, step=0.02, default=0.0),
                    SearchParam(name='rnn_dropout', dtype='float', low=0.0, high=0.2, step=0.02, default=0.0)]
    rnn_cell = keras.layers.LSTMCell

    def __init__(self, input_dim, output_dim, slide_window, hidden_size=128, rnn_dropout=0., fc_dropout=0.):
        super().__init__(input_dim, output_dim, slide_window)
        self.rnn_layer = self.rnn_cell(units=hidden_size, recurrent_dropout=rnn_dropout,
                                       return_sequences=True, return_state=True)
        self.dropout_layer = keras.layers.Dropout(rate=fc_dropout)
        self.fc_layer = keras.layers.Dense(units=hidden_size)

    def call(self, inputs, training=None, mask=None):
        output, final_memory_state, final_carry_state = self.rnn_cell(inputs)
        output = self.dropout_layer(output[:, -1, :])
        output = self.fc_layer(output)
        return output


class RNN(BaseRNN):
    rnn_cell = keras.layers.SimpleRNNCell


class LSTM(BaseRNN):
    rnn_cell = keras.layers.LSTMCell


class GRU(BaseRNN):
    rnn_cell = keras.layers.GRUCell
