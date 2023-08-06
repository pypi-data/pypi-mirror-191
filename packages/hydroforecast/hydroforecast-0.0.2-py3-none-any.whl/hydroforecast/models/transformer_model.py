import torch
import torch.nn as nn
import math

from torch.nn import TransformerEncoderLayer, TransformerEncoder
from visualizer import get_local
from libs.informerlibs.attn import AttentionLayer, ProbAttention
from libs.informerlibs.embed import DataEmbedding
from libs.informerlibs.encoder import EncoderLayer, ConvLayer, Encoder


class PositionalEncoding(nn.Module):

    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        # pe.requires_grad = False
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:x.size(0), :]


class Transformer(nn.Module):
    def __init__(self, c_in, d_model=8, nhead=10, inner_dim=128, num_layers=1, dropout=0.1):
        super(Transformer, self).__init__()
        self.model_type = 'Transformer'
        self.src_mask = None
        self.embedding_layer = nn.Linear(c_in, nhead * d_model)
        self.pos_encoder = PositionalEncoding(nhead * d_model)
        # self.embedding_layer = DataEmbedding(c_in, d_model * nhead, dropout)
        self.encoder_layer = nn.TransformerEncoderLayer(d_model=d_model * nhead, nhead=nhead, dim_feedforward=inner_dim, dropout=dropout,
                                                        batch_first=False)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        self.decoder = nn.Linear(nhead * d_model, 1)
        self.apply(self._weights_init)
        self.init_weights()

    def init_weights(self):
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-0.1, 0.1)

    def _weights_init(self, m):
        # same initialization as keras. Adapted from the initialization developed
        # by JUN KODA (https://www.kaggle.com/junkoda) in this notebook
        # https://www.kaggle.com/junkoda/pytorch-lstm-with-tensorflow-like-initialization
        for name, params in m.named_parameters():
            if "weight_ih" in name:
                nn.init.xavier_normal_(params)
            elif 'weight_hh' in name:
                nn.init.orthogonal_(params)
            elif 'bias_ih' in name:
                params.data.fill_(0)
                # Set forget-gate bias to 1
                n = params.size(0)
                params.data[(n // 4):(n // 2)].fill_(1)
            elif 'bias_hh' in name:
                params.data.fill_(0)

    def forward(self, src):
        src = src.transpose(0, 1)
        if self.src_mask is None or self.src_mask.size(0) != len(src):
            device = src.device

            def generate_square_subsequent_mask(sz):
                mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
                mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
                return mask

            self.src_mask = generate_square_subsequent_mask(len(src)).to(device)
        src = self.embedding_layer(src)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src, self.src_mask)  # , self.src_mask)
        output = self.decoder(output)
        output = output[-1, :, :]
        return output


class MultiAttnRNN(nn.Module):
    def __init__(self, c_in, d_model=8, nhead=10, inner_dim=128, rnn_dim=32, num_layers=1, dropout=0.1):
        super(MultiAttnRNN, self).__init__()
        self.model_type = 'MultiAttnRNN'
        self.src_mask = None
        self.embedding_layer = nn.Linear(c_in, nhead * d_model)
        # self.pos_encoder = PositionalEncoding(nhead * d_model)
        # self.embedding_layer = DataEmbedding(c_in, d_model * nhead, dropout)
        self.encoder_layer = TransformerEncoderLayer(d_model=d_model * nhead, nhead=nhead, dim_feedforward=inner_dim, dropout=dropout,
                                                     batch_first=False)
        self.transformer_encoder = TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        self.gru_layer = nn.LSTM(d_model * nhead, rnn_dim, batch_first=False, bias=True)
        self.fc = nn.Linear(rnn_dim, 1)

    def forward(self, src):
        src = src.transpose(0, 1)
        if self.src_mask is None or self.src_mask.size(0) != len(src):
            device = src.device

            def generate_square_subsequent_mask(sz):
                mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
                mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
                return mask

            self.src_mask = generate_square_subsequent_mask(len(src)).to(device)
        src = self.embedding_layer(src)
        # src = self.pos_encoder(src)
        output = self.transformer_encoder(src, self.src_mask)  # , self.src_mask)
        output, (h, c) = self.gru_layer(output)
        output = self.fc(output[-1, :, :])
        return output


class Informer(nn.Module):
    def __init__(self, c_in, nhead=10, d_model=128, num_layers=1, dropout=0.1):
        super(Informer, self).__init__()
        self.model_type = 'Informer'
        self.embedding_layer = nn.Linear(c_in, nhead * d_model)
        self.pos_encoder = PositionalEncoding(nhead * d_model)
        factor = 5
        d_ff = d_model
        # Encoder
        self.encoder_attn_layers = [EncoderLayer(
            attention=AttentionLayer(ProbAttention(False, factor, attention_dropout=dropout), d_model, nhead),
            d_model=d_model, d_ff=d_ff, dropout=dropout, activation='gelu') for _ in range(num_layers)]
        self.encoder_conv_layers = [ConvLayer(d_model) for _ in range(num_layers - 1)] if num_layers > 1 else None
        self.encoder = Encoder(attn_layers=self.encoder_attn_layers,
                               conv_layers=self.encoder_conv_layers,
                               norm_layer=torch.nn.LayerNorm(d_model))
        self.gru_layer = nn.GRU(d_model, d_model)
        self.fc = nn.Linear(d_model, 1)

    def forward(self, x):
        src = x.transpose(0, 1)
        src = self.embedding_layer(src)
        src = self.pos_encoder(src)
        src = src.transpose(1, 0)
        enc_out, attns = self.encoder(src, attn_mask=None)

        gru_out, _ = self.gru_layer(enc_out)
        return self.fc(gru_out[:, -1, :])
