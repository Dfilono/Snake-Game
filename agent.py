# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:32:55 2022

@author: filon
"""

import torch
import random
import numpy as np
from collections import deque
from SnakeGame_AI_GAME import SnakeGame, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 # Learning Rate

class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 #discount rate, must be smaller than 1
        self.memory = deque(maxlen = MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)
    
    def get_state(self, SnakeGame):
        head = SnakeGame.snake_pos
        point_l = Point(head.x-10, head.y)
        point_r = Point(head.x+10, head.y)
        point_u = Point(head.x, head.y-10)
        point_d = Point(head.x, head.y+10)
        
        dir_l = SnakeGame.direction == Direction.LEFT
        dir_r = SnakeGame.direction == Direction.RIGHT
        dir_u = SnakeGame.direction == Direction.UP
        dir_d = SnakeGame.direction == Direction.DOWN
        
        state = [
            # Danger Straight
            (dir_r and SnakeGame.collision(point_r)) or
            (dir_l and SnakeGame.collision(point_l)) or
            (dir_u and SnakeGame.collision(point_u)) or
            (dir_d and SnakeGame.collision(point_d)),
            
            # Danger Right
            (dir_u and SnakeGame.collision(point_r)) or
            (dir_d and SnakeGame.collision(point_l)) or
            (dir_l and SnakeGame.collision(point_u)) or
            (dir_r and SnakeGame.collision(point_d)),
            
            # Danger Left
            (dir_d and SnakeGame.collision(point_r)) or
            (dir_u and SnakeGame.collision(point_l)) or
            (dir_r and SnakeGame.collision(point_u)) or
            (dir_l and SnakeGame.collision(point_d)),
            
            # Move Direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food Location
            SnakeGame.food_pos.x < SnakeGame.snake_pos.x,
            SnakeGame.food_pos.x > SnakeGame.snake_pos.x,
            SnakeGame.food_pos.y < SnakeGame.snake_pos.y,
            SnakeGame.food_pos.y > SnakeGame.snake_pos.y,
            ]
        
        return np.array(state, dtype = int)
    
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over)) # popleft() if  MAX_MEMORY is reached
    
    def train_long_mem(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tiples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
    
    def train_short_mem(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)
    
    def get_action(self, state):
        # random moves: tradeoff exploration/exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move
    
def train():
    plot_scores =[]
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    while True:
        # get old state
        state_old = agent.get_state(game)
        
        # get move
        final_move = agent.get_action(state_old)
        
        # perform move and get new state
        reward, game_over, score = game.play(final_move)
        state_new = agent.get_state(game)
        
        #train short memory
        agent.train_short_mem(state_old, final_move, reward, state_new, game_over)
        
        #remmeber
        agent.remember(state_old, final_move, reward, state_new, game_over)
        
        if game_over:
            # train the long memory, plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_mem()
            
            if score > record:
                record = score
                agent.model.save()
            
            print('Game: ', agent.n_games, "Score: ",score,'Record: ',record)
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
        

if __name__ == '__main__':
    train()