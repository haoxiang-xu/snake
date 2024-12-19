import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

class SnakeNN(BaseFeaturesExtractor):
    def __init__(self, observation_space, features_dim=256):
        super(SnakeNN, self).__init__(observation_space, features_dim)
        
        input_dim = observation_space.shape[0] * observation_space.shape[1]

        self.mlp = nn.Sequential(
            nn.Flatten(),
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, features_dim)
        )

    def forward(self, observations):
        return self.mlp(observations)