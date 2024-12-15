import gymnasium as gym
import random
from env import SnakeEnv

num_of_players = 1

env = SnakeEnv(num_of_players = num_of_players)

state = env.reset()
finish = False
total_reward = {1: 0, 2: 0, 3: 0, 4: 0}

while not finish:
    env.render(mode='human')
    actions = []
    user_input = input('Enter action for player 1: ')
    if user_input == 'w':
        actions.append(1)
    elif user_input == 's':
        actions.append(2)
    elif user_input == 'a':
        actions.append(3)
    elif user_input == 'd':
        actions.append(4)

    for i in range(2, num_of_players+1):
        actions.append(random.randint(1, 4))
    state, reward, done, _ = env.step(actions)
    for i in range(1, num_of_players+1):
        total_reward[i] += reward[i]
        
    finish = True    
    for i in range(1, num_of_players+1):
       finish = finish and done[i]
        
print('Total reward: ', total_reward)
    
env.close()