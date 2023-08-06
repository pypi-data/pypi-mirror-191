import torch
import torch.nn as nn


class nash_sutcliffe_efficiency(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, real, pred):
        denominator = torch.sum(torch.pow(real - torch.mean(real), 2))
        numerator = torch.sum(torch.pow(pred - real, 2))
        return numerator / denominator
