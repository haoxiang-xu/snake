import numpy as np
import os
import math
import time
import random
import gymnasium as gym
from gymnasium import spaces
from IPython.display import clear_output

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
        
        """ reward parameters ----------------------------------------------------------- """
        self.reward = 0.0
        self.edge_collision_reward = -1.0
        self.self_collision_reward = -1.0
        self.candy_collision_reward = 1.0
        self.max_candy_collision_reward = 10.0
        self.out_of_limit_reward = -1.0
        
        self.candy_collision_multiplier = 1.0
        self.no_candy_collision_turn_count = 0
        
        self.positive_turn_reward = 0.01
        self.negative_turn_reward = -0.009
        self.turn_reward = self.positive_turn_reward
        """ reward parameters ----------------------------------------------------------- """
        
        self.candy_collision_detected = False
        self.pervious_candy_snake_distance = None
        
        self.grid_size = grid_size
        self.max_distance = math.sqrt(grid_size[0]**2 + grid_size[1]**2)
        self.observation_space = spaces.Box(low=0, high=3, shape=(grid_size[0], grid_size[1]), dtype=np.int32)
        
        self.state = np.zeros(self.grid_size, dtype=np.int32)
        self.done = False
    def reset(self, seed=None, options=None):
        def initialize_grid():
            self.snake_position = [(self.grid_size[0]//2, self.grid_size[1]//2), (self.grid_size[0]//2 + 1, self.grid_size[1]//2), (self.grid_size[0]//2 + 2, self.grid_size[1]//2)]
            self.candy_position = []
            np.zeros(self.grid_size, dtype=np.int32)
            for i in range(len(self.snake_position)):
                self.state[self.snake_position[i]] = i + 1
        def calculate_distance_interval():
            head_position = self.snake_position[0]
            candy_position = self.candy_position[0]
            return math.sqrt((head_position[0] - candy_position[0])**2 + (head_position[1] - candy_position[1])**2)
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
        self.pervious_candy_snake_distance = calculate_distance_interval()
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
            self.pervious_candy_snake_distance = calculate_distance_interval(self.snake_position[0])
        def calculate_distance_interval(new_head_position):
            candy_position = self.candy_position[0]
            return math.sqrt((new_head_position[0] - candy_position[0])**2 + (new_head_position[1] - candy_position[1])**2)
        def update_rewards(new_head_position):
            candy_position = self.candy_position[0]
            
            if new_head_position[0] == candy_position[0] and new_head_position[1] == candy_position[1]:
                self.turn_reward = 0
            else:
                current_candy_snake_distance = calculate_distance_interval(new_head_position)
                if current_candy_snake_distance > self.pervious_candy_snake_distance:
                    self.turn_reward = self.negative_turn_reward
                else:
                    self.turn_reward = self.positive_turn_reward
                self.pervious_candy_snake_distance = current_candy_snake_distance
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
            
            update_rewards(new_head_position)
            
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
                self.no_candy_collision_turn_count = 0
                current_candy_reward = self.candy_collision_reward
                self.candy_collision_reward = min(self.max_candy_collision_reward, self.candy_collision_reward * self.candy_collision_multiplier)
                return current_candy_reward
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
        def convert_state_to_observation():
            converted_state = np.zeros(self.grid_size, dtype=np.int32)
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    if self.state[i, j] == 0:
                        converted_state[i, j] = 0
                    elif self.state[i, j] == self.grid_size[0] * self.grid_size[1] + 1:
                        converted_state[i, j] = 3
                    elif self.state[i, j] == 1:
                        converted_state[i, j] = 1
                    else:
                        converted_state[i, j] = 2
            return converted_state
        def truncate():
            if self.no_candy_collision_turn_count > self.grid_size[0] * self.grid_size[1] * 2:
                self.reward = self.out_of_limit_reward
                self.done = True
            else:
                self.no_candy_collision_turn_count += 1
        
        self.reward = move_snake_position(action)
        update_state()
        truncate()
                
        return convert_state_to_observation(), round(self.reward, 4), self.done, False, {}
    def render(self, mode='training', sequential=True):
        def run_in_jupyter():
            try:
                from IPython import get_ipython
                return get_ipython() is not None and 'IPKernelApp' in get_ipython().config
            except ImportError:
                return False
        if mode == 'human':
            if not sequential:
                if run_in_jupyter():
                    clear_output(wait=True)
                else:
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
            print("[Reward: ", round(self.reward, 4), "]")
            if not sequential:
                time.sleep(0.1)
        elif mode == 'auto':
            if not sequential:
                if run_in_jupyter():
                    clear_output(wait=True)
                else:
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
            if not sequential:
                time.sleep(0.32)
        elif mode == 'raw':
            if not sequential:
                if run_in_jupyter():
                    clear_output(wait=True)
                else:
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
            if not sequential:
                time.sleep(0.16)
        else:
            raise ValueError("invalid mode.")
    def close(self): 
        pass