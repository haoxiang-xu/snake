import gymnasium as gym
import random
from env import SnakeEnv

env = SnakeEnv()

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

    for i in range(2, 5):
        actions.append(random.randint(1, 4))
    state, reward, done, _ = env.step(actions)
    for i in range(1, 5):
        total_reward[i] += reward[i]
    finish = done[1] and done[2] and done[3] and done[4]
    
print('Total reward: ', total_reward)
    
env.close()