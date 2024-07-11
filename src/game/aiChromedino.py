# !/usr/bin/python
# -*- coding: utf-8 -*-

# lib
import datetime
import os
import random
import threading
import pygame # type: ignore

from settings import *

#object import Cactus, Bird, Cloud
from objects.obstacles import SmallCactus, LargeCactus, Bird
from objects.aiDinosaur import AiDinosaur
from objects.cloud import Cloud
from evo import mutate

#init
pygame.init()



# MARK: Main
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, distance
    run = True
    clock = pygame.time.Clock()

    agents = [AiDinosaur() for _ in range(10)]
    clouds = [Cloud() for _ in range(3)]
    
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380

    distance = 1
    points = 0

    obstacles = []
    death_count = 0
    
    parentCount = 5
    parents = []

   
    
    nextDistancePerGenerate =800
    nextDistancePerVelocity = 1000
    nextDistancePerPoint =50
    
    def score(nextDistancePerVelocity,nextDistancePerPoint):
        global points, distance, game_speed, highscore
        distance += game_speed

        
        if distance >  nextDistancePerPoint:
            points += 1
            nextDistancePerPoint +=50
        if distance > nextDistancePerVelocity:
            game_speed += 1
            nextDistancePerVelocity +=1000 
            print("faster")

        
        return nextDistancePerVelocity,nextDistancePerPoint


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
    
    def generateObjects(pos):
        switch={
            0:SmallCactus(SMALL_CACTUS, pos), 
            1:LargeCactus(LARGE_CACTUS, pos), 
            2:Bird(BIRD, pos)
        }
        obstacles.append(switch[random.randint(0, 2)])
    generateObjects(SCREEN_WIDTH)
    generateObjects(SCREEN_WIDTH+300)
    while run:
              
        if(distance>nextDistancePerGenerate):
            generateObjects(SCREEN_WIDTH)
            nextDistancePerGenerate+=random.randint(450, 900)
        is_dead = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False      
        
        SCREEN.fill(BACKGROUND_COLOR)
        background()      
        
        #get input
        for agent in agents:
            agent.update(obstacles, game_speed)
        
        #obstacles
        for obstacle in obstacles.copy():
            # Draw call
            obstacle.update(game_speed, obstacles)
            obstacle.draw(SCREEN)
            
            # Collision detection
            for i,agent in enumerate (agents):
                if pygame.sprite.collide_mask(agent, obstacle):
                    agent.dead()
                    if len(agents)<=parentCount:
                        parents.append(agent)
                    agents.pop(i)
                    is_dead = True

            
                    
        #draw call for agents
        #for agent in agents:
            #agent.draw(SCREEN)
        #update score
        nextDistancePerVelocity,nextDistancePerPoint =score(nextDistancePerVelocity,nextDistancePerPoint)        
        #render frame
        
        #generating 
        
        #switch to menu
        """
        if is_dead:
            pygame.time.delay(200)
            menu(death_count)
        """
        clock.tick(FRAME_RATE)
        if len(agents)==0:
            distance = 1
            game_speed = 10
            nextDistancePerGenerate =400
            nextDistancePerVelocity = 1000
            nextDistancePerPoint = 50
            for i,agent in enumerate (parents):
                
                agents.append(agent)
                for j in range(3):
                    agents.append(AiDinosaur())
                    g = mutate(agent.genome)
                    #print(g.all_weights)
                    #print(g.all_biases)
                    agents[len(agents)-1].genomeUpdate(g)
            for i,agent in enumerate (parents):
                parents.pop()
            print (agents)       
              
        agents[0].draw(SCREEN)  
        pygame.display.update()

# MARK: Menu
def menu(death_count):
    global points, highscore
    global FONT_COLOR

    highscore = 0
    run = True
    while run:
        SCREEN.fill(BACKGROUND_COLOR)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()

#start thread
t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
