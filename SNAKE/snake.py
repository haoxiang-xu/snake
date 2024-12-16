import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import torch
from torch import nn
from snake_env import SnakeEnv
import getch

class Snake:
    def __init__(self):
        self.env = SnakeEnv()
    def run(self, model = None):
        def human_run():
            self.env = SnakeEnv()
            state, info = self.env.reset(), {}
            end = False
            total_reward = 0

            while not end:
                self.env.render("human")
                user_pressed_key = getch.getch()
                if user_pressed_key == 'w':
                    action = 0
                elif user_pressed_key == 's':
                    action = 1
                elif user_pressed_key == 'a':
                    action = 2
                elif user_pressed_key == 'd':
                    action = 3
                else:
                    break
                state, reward, done, truncated, _ = self.env.step(action)
                total_reward += reward

                end = done

            if end: 
                print(f"\nSCORE: {total_reward}")
            else:
                print("\nTERMINATED")
            self.env.close()   
        def model_run(model):
            self.env = SnakeEnv()
            state, info = self.env.reset()

            end = False
            total_reward = 0
            
            while not end:
                self.env.render('auto')
                action = model.predict(state)[0]
                state, reward, done, truncated, _ = self.env.step(action)
                total_reward += reward
                end = done or truncated
                
            print(f"\nSCORE: {total_reward}")
            
            self.env.close()
            
        if model is None:
            human_run()
        else:
            model_run(model)
    def training(self, model = None, epochs = 10000):
        if model is None:
            raise ValueError("model or model_path must be provided.")
        model.learn(total_timesteps=epochs)
        return model
            
if __name__ == '__main__':
    # snake = Snake()
    # snake.run()
    snake = Snake()
    #model = DQN.load("snake_model", env = snake.env)
    
    model = DQN("MlpPolicy", snake.env, verbose=1, learning_rate=1e-4, buffer_size=10000)
    
    for i in range(1):
        model = snake.training(model=model, epochs=100000)
        snake.run(model = model)
        
    model.save("snake_model")