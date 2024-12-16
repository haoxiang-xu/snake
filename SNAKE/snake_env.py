import numpy as np
import os
import time
import random
import gymnasium as gym
from gymnasium import spaces

class SnakeEnv(gym.Env):
    metadata = {'render_modes': ['human'], 'render_fps': 30}
    
    def __init__(self, grid_size=(10, 10)):
        super(SnakeEnv, self).__init__()
        def validation_check():
            if not isinstance(grid_size, tuple):
                raise ValueError("grid_size must be a tuple.")
            if len(grid_size) != 2:
                raise ValueError("grid_size must be a tuple of 2 integers.")
            if not all(isinstance(i, int) for i in grid_size):
                raise ValueError("grid_size must be a tuple of 2 integers.")
            if grid_size[0] > 50 or grid_size[1] > 50 or grid_size[0] < 10 or grid_size[1] < 10:
                raise ValueError("grid_size must be a tuple of 2 integers between 10 and 50 exclusively.")
        validation_check()
        
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.action_space = spaces.Discrete(4)
        self.snake_position = []
        self.candy_position = []
        
        """rewards"""
        self.edge_collision_reward = 0
        self.self_collision_reward = 0
        self.candy_collision_reward = 0
        self.turn_reward = 0.256
        self.candy_collision_detected = False
        
        self.grid_size = grid_size
        self.observation_space = spaces.Box(low=0, high=grid_size[0] * grid_size[1] + 1, shape=(grid_size[0], grid_size[1]), dtype=np.int32)
        
        self.state = np.zeros(self.grid_size, dtype=np.int32)
        self.done = False

    def reset(self, seed=None, options=None):
        def initialize_grid():
            self.snake_position = [(self.grid_size[0]//2, self.grid_size[1]//2), (self.grid_size[0]//2 + 1, self.grid_size[1]//2), (self.grid_size[0]//2 + 2, self.grid_size[1]//2)]
            self.candy_position = []
            np.zeros(self.grid_size, dtype=np.int32)
            for i in range(len(self.snake_position)):
                self.state[self.snake_position[i]] = i + 1
        def initialize_candy():
            position_x = random.randint(0, self.grid_size[0] - 1)
            position_y = random.randint(0, self.grid_size[1] - 1)
            
            while self.state[position_x, position_y] != 0:
                position_x = random.randint(0, self.grid_size[0] - 1)
                position_y = random.randint(0, self.grid_size[1] - 1)
            
            if len(self.candy_position) == 0:
                self.candy_position.append((position_x, position_y))
            self.state[position_x, position_y] = self.grid_size[0] * self.grid_size[1] + 1
        
        super().reset(seed=seed)
        initialize_grid()
        initialize_candy()
        self.done = False
        
        return self.state, {}
    
    def step(self, action):
        def initialize_candy():
            position_x = random.randint(0, self.grid_size[0] - 1)
            position_y = random.randint(0, self.grid_size[1] - 1)
            
            while self.state[position_x, position_y] != 0:
                position_x = random.randint(0, self.grid_size[0] - 1)
                position_y = random.randint(0, self.grid_size[1] - 1)
            
            if len(self.candy_position) == 0:
                self.candy_position.append((position_x, position_y))
            self.state[position_x, position_y] = self.grid_size[0] * self.grid_size[1] + 1
        def update_rewards():
            self.edge_collision_reward = len(self.snake_position) - (self.grid_size[0] * self.grid_size[1])
            self.self_collision_reward = len(self.snake_position) - (self.grid_size[0] * self.grid_size[1])
            self.candy_collision_reward = 1
            if self.candy_collision_detected:
                self.candy_collision_detected = False
                self.turn_reward = 0.256
            else:
                self.turn_reward = self.turn_reward / 2     
        def move_snake_position(action):
            if action == 0:
                new_head_position = (self.snake_position[0][0] - 1, self.snake_position[0][1])
            elif action == 1:
                new_head_position = (self.snake_position[0][0] + 1, self.snake_position[0][1])
            elif action == 2:
                new_head_position = (self.snake_position[0][0], self.snake_position[0][1] - 1)
            elif action == 3:
                new_head_position = (self.snake_position[0][0], self.snake_position[0][1] + 1)
            else:
                raise ValueError("invalid action.")
            
            """edge collision check"""
            if new_head_position[0] < 0 or new_head_position[0] >= self.grid_size[0] or new_head_position[1] < 0 or new_head_position[1] >= self.grid_size[1]:
                self.done = True
                return self.edge_collision_reward
            """candy collision check"""
            if self.state[new_head_position] == self.grid_size[0] * self.grid_size[1] + 1:
                self.snake_position = [new_head_position] + self.snake_position
                self.candy_position = []
                initialize_candy()
                self.candy_collision_detected = True
                return self.candy_collision_reward
            else:
                self.snake_position = self.snake_position[:-1]
            """self collision check"""
            if new_head_position in self.snake_position:
                self.done = True
                return self.self_collision_reward
            self.snake_position = [new_head_position] + self.snake_position
            return self.turn_reward
        def update_state():
            self.state = np.zeros(self.grid_size, dtype=np.int32)
            for i in range(len(self.snake_position)):
                self.state[self.snake_position[i]] = i + 1
            for i in range(len(self.candy_position)):
                self.state[self.candy_position[i]] = self.grid_size[0] * self.grid_size[1] + 1
        
        update_rewards()
        reward = move_snake_position(action)
        update_state()
        
        return self.state, reward, self.done, False, {}
    
    def render(self, mode='training'):
        if mode == 'human':
            os.system('cls' if os.name == 'nt' else 'clear')
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    if self.state[i, j] == 0:
                        print('.', end=' ')
                    elif self.state[i, j] == self.grid_size[0] * self.grid_size[1] + 1:
                        print('C', end=' ')
                    else:
                        print('S', end=' ')
                print()
            time.sleep(0.1)
        if mode == 'auto':
            os.system('cls' if os.name == 'nt' else 'clear')
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    if self.state[i, j] == 0:
                        print('.', end=' ')
                    elif self.state[i, j] == self.grid_size[0] * self.grid_size[1] + 1:
                        print('C', end=' ')
                    else:
                        print('S', end=' ')
                print()
            time.sleep(0.5)
        elif mode == 'raw':
            os.system('cls' if os.name == 'nt' else 'clear')
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    if self.state[i, j] == 0:
                        print('.', end=' ')
                    elif self.state[i, j] == self.grid_size[0] * self.grid_size[1] + 1:
                        print('C', end=' ')
                    else:
                        print(self.state[i, j] % 10, end=' ')
                print()
            time.sleep(0.1)
        else:
            print()
    
    def close(self):
        pass