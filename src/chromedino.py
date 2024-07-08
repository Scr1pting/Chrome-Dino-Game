# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading

import pygame # type: ignore

from settings import *

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

        if distance % 50 == 0:
            points += 1

        if distance % 1000 == 0:
            game_speed += 1
        
        with open("../highscore.txt", "w") as f:
            if points >= highscore:
                highscore = points
                f.write(str(highscore))
            f.close()
            
        text1 = font.render(f"HI: {str(5).zfill(5)} ", False, FONT_COLOR_LIGHT)
        text2 = font.render(str(points).zfill(5), False, FONT_COLOR)

        x_pos, y_pos = (760, 40)

        # Get the width of the first text part to calculate the starting position of the second part
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

    while run:
        is_dead = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill(BACKGROUND_COLOR)
        background()

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

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(game_speed, obstacles)

            if pygame.sprite.collide_mask(player, obstacle):
                player.dead()
                is_dead = True
                death_count += 1

        player.draw(SCREEN)

        for cloud in clouds:
            cloud.update(game_speed)
            cloud.draw(SCREEN)

        score()

        pygame.display.update()

        if is_dead:
            pygame.time.delay(2000)
            menu(death_count)

        clock.tick(FRAME_RATE)


# MARK: Menu
def menu(death_count):
    global points, highscore
    global FONT_COLOR

    highscore = 0
    run = True

    with open("../highscore.txt", "r") as f:
        raw_highscore = f.read().strip()
        try:
            highscore = int(raw_highscore)
        except:
            highscore = 0

    while run:
        SCREEN.fill(BACKGROUND_COLOR)
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
