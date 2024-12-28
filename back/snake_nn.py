import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

class ResidualBlock(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, input_dim)
    
    def forward(self, x):
        return x + self.fc2(self.relu(self.fc1(x)))

class SnakeNN(BaseFeaturesExtractor):
    def __init__(self, observation_space, features_dim=256):
        super().__init__(observation_space, features_dim)
        input_dim = observation_space.shape[0] * observation_space.shape[1]

        self.network = nn.Sequential(
            nn.Flatten(),
            ResidualBlock(input_dim),
            nn.ReLU(),
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, features_dim)
        )

    def forward(self, observations):
        return self.network(observations)