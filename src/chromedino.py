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
from objects.dinosaur import Dinosaur
from objects.cloud import Cloud

#init
pygame.init()

def score():
    global points, distance, game_speed, highscore
    distance += game_speed

    font = pygame.font.Font(FONT_FAMILY, 20)
    
    if distance % 50 == 0:
        points += 1

    if distance % 1000 == 0:
        game_speed += 1
    
    with open("../highscore.txt", "w") as f:
        if points >= highscore:
            highscore = points
            f.write(str(highscore))
        
    text1 = font.render(f"HI: {str(5).zfill(5)} ", False, FONT_COLOR_LIGHT)
    text2 = font.render(str(points).zfill(5), False, FONT_COLOR)

    x_pos, y_pos = (760, 40)

    # Get the width of the first text part to calculate
    # the starting position of the second part.
    text_width, _ = text1.get_size()
    x_pos_part2 = x_pos + text_width

    # Blit both parts onto the screen
    SCREEN.blit(text1, (x_pos, y_pos))
    SCREEN.blit(text2, (x_pos_part2, y_pos))

def background():
    global x_pos_bg, y_pos_bg
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg = 0
    x_pos_bg -= game_speed


def restart_screen():
    font = pygame.font.Font(FONT_FAMILY, 25)

    text = font.render("G A M E  O V E R", False, FONT_COLOR)
    textRect = text.get_rect() 
    textRect.center = (SCREEN_WIDTH // 2, 210)
    SCREEN.blit(text, textRect)

    reset_img = RESET
    reset_rect = reset_img.get_rect()
    # Position it at the center of the screen
    reset_rect.center = (SCREEN_WIDTH // 2, 310)  
    SCREEN.blit(reset_img, reset_rect)

    pygame.display.update()

def generateObjects():
    switch = {
        0: SmallCactus(SMALL_CACTUS),
        1: LargeCactus(LARGE_CACTUS),
        2: Bird(BIRD)
    }
    obstacles.append(switch[random.randint(0, 2)])


# MARK: Menu
def menu():
    global highscore
    global FONT_COLOR

    highscore = 0

    #highscore file for memory
    with open("../highscore.txt", "r") as f:
        raw_highscore = f.read().strip()
        try:
            highscore = int(raw_highscore)
        except:
            highscore = 0

    SCREEN.fill(BACKGROUND_COLOR)

    font = pygame.font.Font(FONT_FAMILY, 20)

    text = font.render("Press any Key to Start", False, FONT_COLOR)

    hs_score_text = font.render(
        f"High Score: {highscore}", False, FONT_COLOR
    )

    hs_score_rect = hs_score_text.get_rect()
    hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    SCREEN.blit(hs_score_text, hs_score_rect)

    textRect = text.get_rect() 
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(text, textRect)
    SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return
                

# MARK: Main
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, distance, is_dead
    
    def start():
        global game_speed, obstacles, distance, points, is_dead

        game_speed = 10

        obstacles = []

        distance = 0
        points = 0
        is_dead = False

    run = True
    clock = pygame.time.Clock()

    player = Dinosaur()
    clouds = [Cloud() for _ in range(3)]

    x_pos_bg = 0
    y_pos_bg = 380
    is_dead = True

    menu()
    start()

    while run:
        SCREEN.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        background()

        # Get input
        userInput = pygame.key.get_pressed()
        player.update(userInput)

        if len(obstacles) == 0:
            switch = random.randint(0, 2)
            if switch == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif switch == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif switch == 2:
                obstacles.append(Bird(BIRD))
       
        if len(obstacles) == 0:
            generateObjects()
        
        # Obstacles
        for obstacle in obstacles:
            # Draw call
            obstacle.draw(SCREEN)
            obstacle.update(game_speed, obstacles)
            
            # Collision detection
            if pygame.sprite.collide_mask(player, obstacle):
                player.dead()
                is_dead = True
        
        # Draw call for player
        player.draw(SCREEN)

        # Draw call for clouds
        for cloud in clouds:
            cloud.update(game_speed)
            cloud.draw(SCREEN)
        
        # Update score
        score()

        if is_dead: 
            restart_screen()

            while is_dead:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        start()
                        break
        else:
            pygame.display.update()
        
        clock.tick(FRAME_RATE)

#start thread
t1 = threading.Thread(target=main(), daemon=True)
t1.start()
