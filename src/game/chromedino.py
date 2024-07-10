# Lib
import random
import threading
import pygame

from settings import *
from menus import initial_screen, restart_screen
from scoring import load_highscore, render_score

# Object import Cactus, Bird, Cloud
from objects.obstacles import SmallCactus, LargeCactus, Bird
from objects.dinosaur import Dinosaur
from objects.cloud import Cloud

# Init
pygame.init()


# MARK: Helper Functions
def background():
    global x_pos_bg, y_pos_bg
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg = 0
    x_pos_bg -= game_speed

def generate_objects():
    switch = {
        0: SmallCactus(SMALL_CACTUS),
        1: LargeCactus(LARGE_CACTUS),
        2: Bird(BIRD)
    }
    obstacles.append(switch[random.randint(0, 2)])


# MARK: Main
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, distance, is_dead, nextDistancePerGenerate
    
    def start():
        global game_speed, obstacles, distance, points, is_dead, nextDistancePerGenerate

        game_speed = 10

        obstacles = []

        distance = 0
        points = 0
        is_dead = False

        nextDistancePerGenerate = 0

    run = True
    clock = pygame.time.Clock()

    player = Dinosaur()
    clouds = [Cloud(x=600*i) for i in range(2)]

    x_pos_bg = 0
    y_pos_bg = 380
    is_dead = True
    
    highscore = load_highscore()
    
    initial_screen(highscore)
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
        
        # Object generation
        if(distance > nextDistancePerGenerate):
            generate_objects()
            nextDistancePerGenerate += random.randint(450, 900)
        
        # Obstacles
        for obstacle in obstacles.copy():
            # Draw call
            obstacle.update(game_speed, obstacles)
            obstacle.draw(SCREEN)
            
            # Collision detection
            if pygame.sprite.collide_mask(player, obstacle):
                player.dead()
                is_dead = True
        
        # Draw call for clouds
        for index, cloud in enumerate(clouds):
            prev_cloud = clouds[index - 1]
            cloud.update(game_speed, prev_cloud)
            cloud.draw(SCREEN)

        # Draw call for player
        player.draw(SCREEN)
        
        distance += game_speed

        if distance % 50 == 0:
            points += 1
        if distance % 700 == 0:
            game_speed += 1

        # Update score
        render_score(highscore, points)
        
        if is_dead: 
            restart_screen()

            while is_dead:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        start()
                        break

        pygame.display.update()
        clock.tick(FRAME_RATE)


# Start thread
t1 = threading.Thread(target=main(), daemon=True)
t1.start()
