# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading

import pygame # type: ignore

from settings import *
from collision import check_collision

from objects.obstacles import SmallCactus, LargeCactus, Bird
from objects.dinosaur import Dinosaur
from objects.cloud import Cloud


pygame.init()



# MARK: Main
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, distance
    run = True
    clock = pygame.time.Clock()

    player = Dinosaur()
    clouds = [Cloud() for _ in range(3)]
    
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380

    distance = 0
    points = 0

    font = pygame.font.Font(FONT_FAMILY, 20)
    obstacles = []
    death_count = 0

    def score():
        global points, distance, game_speed, highscore
        distance += game_speed

        if distance % 100 == 0:
            points += 1

        if distance % 3000 == 0:
            game_speed += 1
        
        with open("../highscore.txt", "a") as f:
            if points > highscore:
                highscore = points
                f.write(str(highscore))
            
        text = font.render(f"HI: {str(highscore).zfill(5)} {str(points).zfill(5)}", False, FONT_COLOR)
        
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            switch = random.randint(0, 2)
            if switch == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif switch == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif switch == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(game_speed, obstacles)
            if check_collision(
                player.image,
                (player.dino_rect.x, player.dino_rect.y),
                obstacle.image[0],
                (obstacle.rect.x, obstacle.rect.y)
            ):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        for cloud in clouds:
            cloud.draw(SCREEN)
            cloud.update(game_speed)

        score()

        clock.tick(FRAME_RATE)
        pygame.display.update()


# MARK: Menu
def menu(death_count):
    global points, highscore
    global FONT_COLOR

    highscore = 0
    run = True

    with open("../highscore.txt", "r") as f:
        text = f.read().strip()
        try:
            highscore = int(f.read())
        except ValueError:
            highscore = 0

    while run:
        FONT_COLOR = (83, 83, 83)
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font(FONT_FAMILY, 20)

        if death_count == 0:
            text = font.render("Press any Key to Start", False, FONT_COLOR)
        elif death_count > 0:
            text = font.render("Press any Key to Restart", False, FONT_COLOR)
            score = font.render(f"Your Score: {points}", False, FONT_COLOR)

            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
