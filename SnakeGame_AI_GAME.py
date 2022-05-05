# -*- coding: utf-8 -*-
"""
Created on Wed May  4 21:44:21 2022

@author: filon
"""

import pygame
import time
import random
import numpy as np

# Intialize pygame
pygame.init()
font = pygame.font.SysFont('times new roman',20)
snake_speed = 15

# window size
wx = 720
wy = 480

# define colors
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)

class SnakeGame:
    
    def __init__(self,w=wx,h=wy):
        self.w = w
        self.h = h
        # Initialize game window
        pygame.display.set_caption("Snake")
        self.game_window = pygame.display.set_mode((self.w,self.h))
        # FPS
        self.fps = pygame.time.Clock()
        self.reset()
        
        
    def reset(self):
        # Init game state
        #Set default snake direction
        self.direction = 'RIGHT'
        self.change_to = self.direction
        
        # Define snake position
        self.snake_pos = [100,50]

        # Define head
        self.snake_body = [[100,50],[90,50],[80,50],[70,50]]
        
        # Score Board
        self.score = 0
        
        #Food init
        self.food_spawn = False
        self.place_food()
        self.frame_iteration = 0
        
    def place_food(self):
        # Food position
        self.food_pos = [random.randrange(1, (self.w//10))*10,random.randrange(1,(self.h//10))*10]
        self.food_spawn = True
        if self.food_pos in self.snake_body:
            self.place_food()

    def play(self,action):
        self.frame_iteration += 1
        # Collect input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # move
        self.move(action)
        self.snake_body.insert(0, self.snake_pos)
        
        # Game Over Conditions
        reward = 0
        game_over = False
        if self.collision() or self.frame_iteration > 100*len(self.snake_body):
            game_over = True
            reward = -10
            return game_over, self.score, reward
                
        #Place new food
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 10
            reward = 10
            self.food_spawn = False
        else:
            self.snake_body.pop()
        
        if not self.food_spawn:
            self.place_food()
         
        self.fps.tick(snake_speed)
        self.update_ui()
        return game_over, self.score, reward
    
    def move(self, action):
        clock_wise = ["Right","DOWN","LEFT","UP"]
        idx = clock_wise.index(self.change_to)
        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx] #no change
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx+1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx-1) % 4
            new_dir = clock_wise[next_idx]
        
        self.change_to = new_dir
        
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        # Moving the snake
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10
          
    def update_ui(self):
        self.game_window.fill(black)
        # Snake body growing
        self.snake_body.insert(0,list(self.snake_pos))
                
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window,green,pygame.Rect(pos[0],pos[1],10,10))
            
        pygame.draw.rect(self.game_window,white,pygame.Rect(self.food_pos[0],self.food_pos[1],10,10))
        text = font.render("Score: "+str(self.score),True,white)
        self.game_window.blit(text,[0,0])
        pygame.display.flip()
    
    def collision(self, pt=None):
        if pt is None:
            pt = self.snake_pos
        if self.pt[0] < 0 or self.pt[0] > self.w-10:
            return True
        if self.pt[1] < 0 or self.pt[1] > self.h-10:
            return True
        if self.pt in self.snake_body[1:]:
            return True
        
        return False
    
    