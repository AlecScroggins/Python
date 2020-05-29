# -*- coding: utf-8 -*-
"""
Created on Tue May 19 10:57:03 2020

@author: ascroggins
"""
# keep score  
# get username
#record scores in file 
#when score reaches certian point increase speed
import pygame
import sys
import random 

#funtions
def drop_enemies(enemy_list):
    delay = random.random() # random float between 0 and 1 with equal probabilities, used to stagger enemy drop
    num_enemies = 7
    delay_metric = .2
    if len(enemy_list) < num_enemies and delay < delay_metric:
        x_pos = random.randint(0,width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])
        

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    
    e_y = enemy_pos[1]
    e_x = enemy_pos[0]
    
    #two ways x coordinate could overlap
    if (e_x >= p_x) and (e_x < p_x+player_size) or (p_x >= e_x) and (p_x < e_x+ enemy_size):
        # checks for y overlap
        if (e_y >= p_y) and (e_y < p_y + player_size) or (p_y >= e_y) and (p_y <e_y + enemy_size ):
            return True
    return False


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen,enemy_color, (enemy_pos[0], enemy_pos[1], enemy_size,enemy_size))
        
def update_enemy_pos(enemy_list, score):
        #update positon of enemy
    for indx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(indx)
            score += 1
    return score

            
def set_level(score, SPEED):
 
    if score <20:
        SPEED = 5
    elif score <60:
        SPEED = 7
    elif score < 150:
        SPEED = 10
    elif score < 300:
        SPEED = 13
    elif score < 500:
        SPEED = 15
    else:
        SPEED = 17

    return SPEED
    

stop = None   
while stop  == None:   
    #variables
    pygame.init() #creates screen
    
    # speed
    SPEED =5
    FRAME_RATE = 40
    #screen size
    width = 800
    height = 600# in pixels
    
    #colors
    player_color = [20,90,133]
    enemy_color=  [0,0,0]
    yellow = (255,255,0)
    background_color = (255,255,255)
    
    #player metrics
    player_size = 50
    player_pos = [width/2,height-2*player_size]
    
    #enemy metrics
    enemy_size = 50
    rand_num = random.randint(0,width-enemy_size)
    
    enemy_pos = [rand_num,0] #width/ height
    enemy_list = [enemy_pos]
    
    # main body
    screen = pygame.display.set_mode((width, height))#sets hieght and width of screen
    game_over = False
    clock = pygame.time.Clock()
    
    myfont = pygame.font.SysFont("monospace", 35)
    
    score = 0
    username = input("Enter username: ")
    while not game_over:
        for event in pygame.event.get(): #tracks mouse movement on screen
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                x = player_pos[0]
                y = player_pos[1]
                if event.key == pygame.K_LEFT:#moves block
                    x-=player_size
                elif event.key == pygame.K_RIGHT:
                    x+=player_size
                player_pos = [x,y]
                
        screen.fill((background_color)) # fills rest of screen in black
       
        
        
       
        drop_enemies(enemy_list) 
        score = update_enemy_pos(enemy_list, score)
        SPEED = set_level(score, SPEED)
        
        text = "Score:" + str(score)
        label = myfont.render(text, 1, player_color)
        screen.blit(label, (width-200, height-40))
        
        if collision_check(enemy_list, player_pos):
            highscore = open("highscore.txt", "a+")
            highscore.write(str(score)+", " + username + "\n")
            highscore.close()
            game_over = True
            break
        draw_enemies(enemy_list)
        
        pygame.draw.rect(screen, player_color,(player_pos[0],player_pos[1], player_size,player_size))
        clock.tick(FRAME_RATE)
        
        pygame.display.update()