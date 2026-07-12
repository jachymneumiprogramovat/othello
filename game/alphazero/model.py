import torch
from torch import nn
import torch.nn.functional as F

from alpha_constants import *

class HiddenLayer(nn.Module):
    def __init__(self,num_channels:int):
        super().__init__()
        self.conv1 = nn.Conv1d(num_channels, num_channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(num_channels)
        self.conv2 = nn.Conv1d(num_channels, num_channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(num_channels)

    def forward(self, x):
        residual = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += residual
        x = F.relu(x)

        return x


class PolicyHead(nn.Module):
    """
    Predicts move policies, outputs the raw values wihout masking illegal moves
    or softmaxing.
    """

    def __init__(self, num_channels: int, action_size: int):
        super().__init__()
        self.conv = nn.Conv1d(num_channels, 32, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm1d(32)
        self.fc = nn.Linear(32 * rows * cols, action_size)

    def forward(self, x):
        x = F.relu(self.bn(self.conv(x)))
        x = x.view(x.size(0), -1)
        return self.fc(x)

class ScoreHead(nn.Module):
    """
    Predicts a single scalar evaluation of the position, in [-1, 1]:
    -1 = certain loss for the side to move, +1 = certain win.
    """

    def __init__(self, num_channels: int):
        super().__init__()
        self.conv = nn.Conv1d(num_channels, 3, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm1d(3)
        self.fc = nn.Linear(3 * rows * cols, 1)

    def forward(self, x):
        x = F.relu(self.bn(self.conv(x)))
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return torch.tanh(x)

class Model(nn.Module):
    """
    Shared convolutional trunk (a start block followed by stacked ResBlock
    hidden layers) feeding into a PolicyHead and a ScoreHead.
    """

    def __init__(self, num_channels: int, num_hidden: int, device: str):
        super().__init__()
        self.device = device

        self.start_block = nn.Sequential(
            nn.Conv1d(INPUT_CHANNELS, num_channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(num_channels),
            nn.ReLU(),
        )

        self.hidden_layers = nn.ModuleList(
            [HiddenLayer(num_channels) for _ in range(num_hidden)]
        )

        self.policy_head = PolicyHead(num_channels, (rows*cols)+1) # wholle board plus skip
        self.score_head = ScoreHead(num_channels)

        self.to(device)

    def forward(self, x):
        x = self.start_block(x)
        for layer in self.hidden_layers:
            x = layer(x)

        policy = self.policy_head(x)
        score = self.score_head(x)
        return policy, score
