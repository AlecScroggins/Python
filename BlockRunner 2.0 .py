# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:55:35 2020

@author: ascroggins
"""


import pygame
import random
import sys


  
# functions
def move_player(player_pos):
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
            elif event.key == pygame.K_UP:
                y-= player_size
            elif event.key == pygame.K_DOWN:
                y+= player_size
                
            player_pos = [x,y]
    return player_pos


def enemy_spawn_coordinates(num): # creates spawn zone coordinates
    if num == 1:
        zone = [random.randint(0,width - enemy_size), 0 ] # top of screen, x, y coordinates
    elif num == 2:
        zone = [width- enemy_size, random.randint(0,height - enemy_size) ] # right side
    elif num == 3:
        zone = [random.randint(0,width - enemy_size), height - enemy_size]# bottom
    elif num == 4:
        zone = [0, random.randint(0,height-enemy_size)]# Left
    return zone 

def draw_enemies(enemy_list):
    #if len(enemy_list)< max_enemies:
      #  enemy_pos = enemy_spawn_coordinates(width, height, enemy_size) #if the liost is shorter than the max enemies, spawn new enemies at point
      #  enemy_list.append(enemy_pos)
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, enemy_color, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))# draw all enemies in list
    return enemy_list

def draw_enemy(enemy_pos):
    pygame.draw.rect(screen, enemy_color, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))# draw all enemies in list
        

def create_top_enemies(top_enemy_list):#checks if enough eneies on screen, if not generates them
    delay = random.random()
    if len(top_enemy_list) < max_enemies and delay < throttle:
        new_enemy = enemy_spawn_coordinates(1)
        top_enemy_list.append(new_enemy)
    return top_enemy_list
        
def update_top_enemy_pos(top_enemy_list): #if enemy is on screen updates position, if not removes from list
    for ind, enemy_pos in enumerate(top_enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] +=speed
            draw_enemy(enemy_pos)
        else:
            top_enemy_list.pop(ind)
    return top_enemy_list
            
def create_right_enemies(right_enemy_list):
        delay = random.random()
        if len(right_enemy_list) < max_enemies and delay < throttle:
            new_enemy = enemy_spawn_coordinates(2)
            right_enemy_list.append(new_enemy)
        return right_enemy_list
    
def update_right_enemy_pos(right_enemy_list):
    for ind, enemy_pos in enumerate(right_enemy_list):
        if enemy_pos[0] <=width-enemy_size and enemy_pos[0] > 0 :
            enemy_pos[0] -=speed
            draw_enemy(enemy_pos)
        else:
            right_enemy_list.pop(ind)
    return right_enemy_list
     
       



def collision_check(player_pos, e_list, e_size, p_size):
    for e_pos in e_list:
        p_x = player_pos[0]
        p_y = player_pos[1]
        
        
        e_x = e_pos[0]
        e_y = e_pos[1]
        
        #two ways x coordinate could overlap
        if (e_x >= p_x) and (e_x < p_x+p_size) or (p_x >= e_x) and (p_x < e_x+ e_size):
            # checks for y overlap
            if (e_y >= p_y) and (e_y < p_y + p_size) or (p_y >= e_y) and (p_y <e_y + e_size ):
                return True
        return False



def create_new_food():
    rand1 = random.randint(20,width-20)
    rand2  = random.randint(20,height-20)
    
    x = rand1
    y= rand2
    food_coordinates = [[x,y]]
    return food_coordinates

def update_food(food_coordinates):
    pygame.draw.rect(screen, food_color, (food_coordinates[0][0], food_coordinates[0][1], food_size, food_size))


stop = None
while stop == None:
    pygame.init()
    #variables     
    throttle = .01 #creates varability in block creation
    
    #inital enemy lists
    top_enemy_list = [] 
    right_enemy_list  =[]
    bottom_enemy_list = []
    left_enemy_list = []

    
    
    #screen
    FRAME_RATE = 30
    width = 800
    height= 600
    
    #player dimentions
    player_color = (20,90,133)
    player_size = 40
    player_pos = [width/2, height/2]
    
    #enemy metrics
    enemy_list = []
    max_enemies = 6
    enemy_size = 50
    enemy_color = (0,0,0)
    speed = 5
    throttle = .05 #enemy variability higher will have more clusters
    
    master_list=[]
    #food
    food_size = 10
    food_color = (20,90,133)
    #background
    background_color = (255,255,255)


    score = 0
    #main body
    
    screen = pygame.display.set_mode((width, height))
    screen.fill((background_color))
    clock = pygame.time.Clock()
    game_over = False
    food_coordinates = [[width/3, height/3]]
    
    myfont = pygame.font.SysFont("monospace", 35)
    
    
    while game_over == False:

           
        #Update Player
        new_coordinates = move_player(player_pos) # gets new player coordinate sbased on keyboard
        player_pos[0] = new_coordinates[0]# updates player coordinates
        player_pos[1] = new_coordinates[1]
        screen.fill((background_color)) # fills rest of screen  
        pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size)) # draws player
        
        # top enemy
        top_enemy_list = create_top_enemies(top_enemy_list)
        update_top_enemy_pos(top_enemy_list)
        # right_ enemy
        right_enemy_list = create_right_enemies(right_enemy_list)
        update_right_enemy_pos(right_enemy_list)
        
       
        if collision_check( player_pos, top_enemy_list, enemy_size, player_size) == True:
            game_over = True
            break
        if  collision_check(player_pos, right_enemy_list, enemy_size, player_size) == True:
            game_over  = True
            break
        
        if collision_check(player_pos, food_coordinates, food_size, player_size) == True:
           food_coordinates = create_new_food()
           player_size +=0
           enemy_size-=0
           score +=1
        

        update_food(food_coordinates)
        
  
        text = "Score:" + str(score)
        label = myfont.render(text, 1, player_color)
        screen.blit(label, (width-200, height-40))
        clock.tick(FRAME_RATE)
        pygame.display.update() # updates screen
        
