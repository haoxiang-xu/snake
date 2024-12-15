import gymnasium as gym
import random
from env import SnakeEnv

env = SnakeEnv()

state = env.reset()
finish = False
total_reward = {1: 0, 2: 0, 3: 0, 4: 0}

while not finish:
    env.render()
    actions = []
    for i in range(1, 5):
        actions.append(random.randint(1, 4))
    state, reward, done, _ = env.step(actions)
    for i in range(1, 5):
        total_reward[i] += reward[i]
    finish = done[1] and done[2] and done[3] and done[4]
    
print('Total reward: ', total_reward)
    
env.close()