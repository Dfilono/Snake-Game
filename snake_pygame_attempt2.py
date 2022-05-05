# -*- coding: utf-8 -*-
"""
Created on Wed May  4 20:25:36 2022

@author: filon
"""

import pygame
import time
import random

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

# Intialize pygame
pygame.init()

# Initialize game window
pygame.display.set_caption("Snake")
game_window = pygame.display.set_mode((wx,wy))

# FPS
fps = pygame.time.Clock()

# Define snake position
snake_pos = [100,50]

# Define head
snake_body = [[100,50],[90,50],[80,50],[70,50]]

# Food position
food_pos = [random.randrange(1, (wx//10))*10,random.randrange(1,(wy//10))*10]
food_spawn = True

#Set default snake direction
direction = 'RIGHT'
change_to = direction

# Score Board
score = 0

def show_score(choice,color,font,size):
    score_font = pygame.font.SysFont(font,size)
    score_surface = score_font.render("Score :"+str(score),True,color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface,score_rect)
    
# Game Over
def game_over():
    my_font = pygame.font.SysFont("times new toman", 50)
    game_over_surface = my_font.render('Your Score is: ' + str(score),True,red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop=(wx/2,wy/2)
    game_window.blit(game_over_surface,game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
    
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
        
    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10
    
    # Snake body growing
    snake_body.insert(0,list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        food_spawn = False
    else:
        snake_body.pop()
    
    if not food_spawn:
        food_pos = [random.randrange(1, (wx//10))*10,random.randrange(1,(wy//10))*10]
        
    food_spawn = True
    game_window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(game_window,green,pygame.Rect(pos[0],pos[1],10,10))
    
    pygame.draw.rect(game_window,white,pygame.Rect(food_pos[0],food_pos[1],10,10))
    
    # Game Over Conditions
    if snake_pos[0] < 0 or snake_pos[0] > wx-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > wy-10:
        game_over()
    
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
    
    show_score(1,white,'times new roman', 20)
    
    pygame.display.update()
    
    fps.tick(snake_speed)