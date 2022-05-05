# -*- coding: utf-8 -*-
"""
Created on Wed May  4 21:44:21 2022

@author: filon
"""

import pygame
import time
import random

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
        
    def place_food(self):
        # Food position
        self.food_pos = [random.randrange(1, (self.w//10))*10,random.randrange(1,(self.h//10))*10]
        self.food_spawn = True
        if self.food_pos in self.snake_body:
            self.place_food()

    def play(self):
        # Collect input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    self.change_to = 'RIGHT'
        
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
        
        # Game Over Conditions
        game_over = False
        if self.collision():
            game_over = True
            return game_over, self.score
                
        #Place new food
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 10
            self.food_spawn = False
        else:
            self.snake_body.pop()
        
        if not self.food_spawn:
            self.place_food()
         
        self.fps.tick(snake_speed)
        self.update_ui()
        return game_over, self.score
          
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
    
    def collision(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.w-10:
            return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.h-10:
            return True
        if self.snake_pos in self.snake_body[1:]:
            return True
        
        return False

if __name__ == '__main__':
    game = SnakeGame()
    # Main Loop
    while True:
        game_over, score = game.play()
        if game_over == True:
            break
    print('Final Score',score)
    pygame.quit()
    
    