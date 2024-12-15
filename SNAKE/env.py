import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
import os
import time

class SnakeEnv(gym.Env):
    metadata = {'render_modes': ['human'], 'render_fps': 30}
    
    def __init__(self, num_of_players = 4, grid_size = (10, 10)):
        def validation_check():
            if num_of_players <= 0 or num_of_players > 4:
                raise ValueError('number of players must be between 1 and 4.')
            if grid_size[0] < 10 or grid_size[1] < 10:
                raise ValueError('grid size must be at least 10 x 10.')
        
        validation_check()
        super(SnakeEnv, self).__init__()
        
        self.num_of_players = num_of_players
        self.candies_indicator = 1
        self.player_positions = {1: [], 2: [], 3: [], 4: []}
        self.indicators = {
            1: {"head": 2, "body": 3},
            2: {"head": 4, "body": 5},
            3: {"head": 6, "body": 7},
            4: {"head": 8, "body": 9}
        }
        
        self.actions = {
            1: 'UP',
            2: 'DOWN',
            3: 'LEFT',
            4: 'RIGHT'
        }
        self.action_space = spaces.Discrete(5)
        
        self.grid_size = grid_size
        self.observation_space = spaces.Box(low = 0, high = 9, shape = (self.grid_size[0], self.grid_size[1]), dtype = np.uint8)
        
        self.state = None
        if self.num_of_players == 1:
            self.done = {1: False}
        elif self.num_of_players == 2:
            self.done = {1: False, 2: False}
        elif self.num_of_players == 3:
            self.done = {1: False, 2: False, 3: False}
        elif self.num_of_players == 4:
            self.done = {1: False, 2: False, 3: False, 4: False}
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = self._initiallize_grid()
        return self.state
    
    def _initiallize_grid(self):
        grid = np.zeros(self.grid_size)
        self.player_positions = {
            1: [[2, 1], [1,1]], 
            2: [[self.grid_size[0] - 2, 2], [self.grid_size[0] - 2, 1]], 
            3: [[self.grid_size[0] - 3, self.grid_size[1] - 2], [self.grid_size[0] - 2, self.grid_size[1] - 2]], 
            4: [[1, self.grid_size[1] - 3], [1, self.grid_size[1] - 2]]
        }

        def generate_players():
            for player in range(1, self.num_of_players+1):
                grid[self.player_positions[player][0][0], self.player_positions[player][0][1]] = self.indicators[player]['head']
                grid[self.player_positions[player][1][0], self.player_positions[player][1][1]] = self.indicators[player]['body']
        def generate_canides():
            candies_to_generated = self.num_of_players
            
            while candies_to_generated > 0:
                x = random.randint(0, self.grid_size[0]-1)
                y = random.randint(0, self.grid_size[1]-1)
                if grid[x, y] == 0:
                    grid[x, y] = self.candies_indicator
                    candies_to_generated -= 1
        
        generate_players()
        generate_canides()
        
        return grid    
        
    def step(self, actions):
        reward = self._take_action(actions)        
        return self.state, reward, self.done, {}
    
    def _take_action(self, actions):
        def validate_check(actions):
            if len(actions) != self.num_of_players:
                raise ValueError('number of actions must be equal to number of players.')
            for action in actions:
                if action not in self.actions:
                    raise ValueError('invalid action.')
        def update_player_positions(player):
            not_allowed_direction = self.player_positions[player][1]
            if actions[player-1] == 1:
                next_position  = [self.player_positions[player][0][0] - 1, self.player_positions[player][0][1]]
            elif actions[player-1] == 2:
                next_position  = [self.player_positions[player][0][0] + 1, self.player_positions[player][0][1]]
            elif actions[player-1] == 3:
                next_position  = [self.player_positions[player][0][0], self.player_positions[player][0][1] - 1]
            elif actions[player-1] == 4:
                next_position  = [self.player_positions[player][0][0], self.player_positions[player][0][1] + 1]
            
            # self collision check
            if next_position[0] == not_allowed_direction[0] and next_position[1] == not_allowed_direction[1]:
                rewards[player] = self.grid_size[0] * self.grid_size[1] * -1
                self.done[player] = True
                for position in self.player_positions[player]:
                    if position[0] >= 0 and position[0] < self.grid_size[0] and position[1] >= 0 and position[1] < self.grid_size[1]:
                        self.state[position[0], position[1]] = 0
                return 0
            
            self.player_positions[player].insert(0, next_position)
            if next_position[0] >= 0 and next_position[0] < self.grid_size[0] and next_position[1] >= 0 and next_position[1] < self.grid_size[1]:
                if self.state[next_position[0], next_position[1]] == self.candies_indicator:
                    return 1
                else:
                    self.state[self.player_positions[player][-1][0], self.player_positions[player][-1][1]] = 0
                    self.player_positions[player] = self.player_positions[player][:-1]
                    return 0
            return 0
        def update_grid(player):
            next_position = self.player_positions[player][0]
            pervious_head_position = self.player_positions[player][1]
            # edge collision check
            if next_position[0] < 0 or next_position[0] >= self.grid_size[0] or next_position[1] < 0 or next_position[1] >= self.grid_size[1]:
                rewards[player] = self.grid_size[0] * self.grid_size[1] * -1
                self.done[player] = True
                for position in self.player_positions[player]:
                    if position[0] >= 0 and position[0] < self.grid_size[0] and position[1] >= 0 and position[1] < self.grid_size[1]:
                        self.state[position[0], position[1]] = 0
            # candy collision check
            elif self.state[next_position[0], next_position[1]] == self.candies_indicator:
                rewards[player] = 1
                self.state[next_position[0], next_position[1]] = self.indicators[player]['head']
                self.state[pervious_head_position[0], pervious_head_position[1]] = self.indicators[player]['body']
            # body collision check
            elif self.state[next_position[0], next_position[1]] != 0:
                rewards[player] = self.grid_size[0] * self.grid_size[1] * -1
                self.done[player] = True
                for position in self.player_positions[player]:
                    if position[0] >= 0 and position[0] < self.grid_size[0] and position[1] >= 0 and position[1] < self.grid_size[1]:
                        self.state[position[0], position[1]] = 0
            else:
                self.state[next_position[0], next_position[1]] = self.indicators[player]['head']
                self.state[pervious_head_position[0], pervious_head_position[1]] = self.indicators[player]['body']     
        def terminal_state_check():
            if self.num_of_players == 1:
                return 0
            terminated_players = 0
            for player in range(1, self.num_of_players+1):
                if self.done[player]:
                    terminated_players += 1
            if terminated_players == self.num_of_players - 1:
                for player in range(1, self.num_of_players+1):
                    if not self.done[player]:
                        rewards[player] = self.grid_size[0] * self.grid_size[1]
                        self.done[player] = True
        
        validate_check(actions)
        
        candies_to_generated = 0
        rewards = {1: 0, 2: 0, 3: 0, 4: 0}
        
        for player in range(1, self.num_of_players+1):
            if self.done[player]:
                continue
            candies_to_generated += update_player_positions(player)
        for player in range(1, self.num_of_players+1):
            if self.done[player]:
                continue
            update_grid(player)
            
        print(self.player_positions[1])
            
            
        if candies_to_generated > 0:
            while candies_to_generated > 0:
                x = random.randint(0, self.grid_size[0]-1)
                y = random.randint(0, self.grid_size[1]-1)
                if self.state[x, y] == 0:
                    self.state[x, y] = self.candies_indicator
                    candies_to_generated -= 1

        terminal_state_check()
        return rewards
                
    def render(self, mode='raw'):
        def render_raw_grid():
            print(self.state)
        def render_human_readable_grid():
            symbols = {
                0: ' ',
                1: 'O',
                2: '1',
                3: '1',
                4: '2',
                5: '2',
                6: '3',
                7: '3',
                8: '4',
                9: '4'
            }
            os.system('cls' if os.name == 'nt' else 'clear')

            for x in range(self.grid_size[0]):
                for y in range(self.grid_size[1]):
                    print(symbols.get(self.state[x, y], '?'), end=' ')
                print()

            time.sleep(0.1)
        
        if mode == 'raw':
            render_raw_grid()
        elif mode == 'human':
            render_human_readable_grid()
    
    def close(self):
        pass