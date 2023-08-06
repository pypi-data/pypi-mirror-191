import torch.nn as nn


class MultiheadAttentionLSTM(nn.Module):
    def __init__(self, c_in, c_out, num_heads, embed_dim, output_dim, dropout=0.):
        super().__init__()
        self.input_layer = nn.Linear(in_features=c_in, out_features=embed_dim)
        self.attention_layer = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, batch_first=True)
        self.lstm_layer = nn.LSTM(embed_dim, output_dim)
        self.dropout_layer = nn.Dropout(p=dropout)
        self.fc = nn.Linear(output_dim, c_out)

    def forward(self, x):
        x = self.input_layer(x)
        attn_output, attn_output_weights = self.attention_layer(x, x, x)
        rnn_output, _ = self.lstm_layer(attn_output)
        rnn_output = rnn_output[:, -1]
        return self.fc(self.dropout_layer(rnn_output))

    def return_score_weight(self, x):
        attn_output, attn_output_weights = self.attention_layer(x, x, x)
        return attn_output, attn_output_weights


