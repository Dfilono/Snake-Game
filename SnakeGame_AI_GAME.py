# -*- coding: utf-8 -*-
"""
Created on Wed May  4 21:44:21 2022

@author: filon
"""

import pygame
import time
import random
import numpy as np
from enum import Enum
from collections import namedtuple

# Intialize pygame
pygame.init()
font = pygame.font.SysFont('times new roman',20)
snake_speed = 60

# window size
wx = 720
wy = 480

# define colors
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)

Point = namedtuple("Point",'x,y')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

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
        self.direction = Direction.RIGHT
        
        # Define snake position
        self.snake_pos = Point(self.w/2, self.h/2)

        # Define head
        self.snake_body = [self.snake_pos,
                           Point(self.snake_pos.x - 10, self.snake_pos.y),
                           Point(self.snake_pos.x - 20, self.snake_pos.y)]
        
        # Score Board
        self.score = 0
        
        #Food init
        self.food_pos = None
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        # Food position
        x = random.randrange(0, (self.w//10))*10
        y = random.randrange(0, (self.h//10))*10
        self.food_pos = Point(x,y)
        if self.food_pos in self.snake_body:
            self._place_food()

    def play(self, action):
        self.frame_iteration += 1
        # Collect input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # move
        self._move(action)
        self.snake_body.insert(0, self.snake_pos)
        
        # Game Over Conditions
        reward = 0
        game_over = False
        if self.collision() or self.frame_iteration > 100*len(self.snake_body):
            game_over = True
            reward = -10
            return reward, game_over, self.score
                
        #Place new food
        if self.snake_pos == self.food_pos:
            self.score += 10
            reward = 10
            self._place_food()
        else:
            self.snake_body.pop()
         
        self.update_ui()
        self.fps.tick(snake_speed)
        return reward, game_over, self.score 
    
    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx] #no change
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx+1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx-1) % 4
            new_dir = clock_wise[next_idx]
        
        self.direction = new_dir
        
        x = self.snake_pos.x
        y = self.snake_pos.y
        
        if self.direction == Direction.RIGHT:
            x += 10
        elif self.direction == Direction.LEFT:
            x -= 10
        elif self.direction == Direction.DOWN:
            y += 10
        elif self.direction == Direction.UP:
            y -= 10
            
        self.snake_pos = Point(x,y)
          
    def update_ui(self):
        self.game_window.fill(black)
        # Snake body growing
        #self.snake_body.insert(0,list(self.snake_pos))
                
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window,green,pygame.Rect(pos.x,pos.y,10,10))
            
        pygame.draw.rect(self.game_window,white,pygame.Rect(self.food_pos.x,self.food_pos.y,10,10))
        text = font.render("Score: "+str(self.score),True,white)
        self.game_window.blit(text,[0,0])
        pygame.display.flip()
    
    def collision(self, pos=None):
        if pos is None:
            pos = self.snake_pos
        if pos.x < 0 or pos.x > self.w-10 or pos.y < 0 or pos.y > self.h-10 :
            return True
        if pos in self.snake_body[1:]:
            return True
        
        return False
    
    