# Lib
import random
import threading
import pygame

from settings import *
from menus import initial_screen, restart_screen
from scoring import load_highscore, draw_score

# Object import Cactus, Bird, Cloud
from objects.obstacles import Obstacle, SmallCactus, LargeCactus, Bird
from objects.dinosaur import Dinosaur
from objects.cloud import Cloud

from background import draw_ground, draw_clouds

# Init
pygame.init()

class Game:
    def __init__(self) -> None:
        self.speed = 10
        self.obstacles = []

        self.distance = 0
        self.points = 0
        self.is_dead = False

        self.next_generate_distance = 0


def generate_obstacles(obstacles: list[Obstacle]):
    switch = {
        0: SmallCactus(SMALL_CACTUS),
        1: LargeCactus(LARGE_CACTUS),
        2: Bird(BIRD)
    }
    obstacles.append(switch[random.randint(0, 2)])


# MARK: Main
def main():
    global obstacles
    
    clock = pygame.time.Clock()

    player = Dinosaur()
    clouds = [Cloud(x=600*i) for i in range(2)]

    x_pos_bg = 0
    y_pos_bg = 380
    is_dead = False
    
    highscore = load_highscore()
    initial_screen(highscore)

    game = Game()

    while True:
        SCREEN.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        x_pos_bg = draw_ground(x_pos_bg, y_pos_bg, game.speed)
        draw_clouds(clouds, game.speed)

        # Get input
        userInput = pygame.key.get_pressed()
        player.update(userInput)
        
        # Object generation
        if game.distance > game.next_generate_distance:
            generate_obstacles(game.obstacles)
            game.next_generate_distance += random.randint(450, 900)
        
        # Obstacles
        for obstacle in game.obstacles.copy():
            # Draw call
            obstacle.update(game.speed, game.obstacles)
            obstacle.draw(SCREEN)
            
            # Collision detection
            if pygame.sprite.collide_mask(player, obstacle):
                player.dead()
                is_dead = True

        # Draw call for player
        player.draw(SCREEN)
    
        game.distance += game.speed

        if game.distance % 50 == 0:
            game.points += 1
        if game.distance % 700 == 0:
            game.speed += 1

        # Update score
        draw_score(highscore, game.points)
        
        if is_dead: 
            restart_screen()

            while is_dead:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        game = Game()
                        is_dead = False
                        break

        pygame.display.update()
        clock.tick(FRAME_RATE)


# Start thread
t1 = threading.Thread(target=main(), daemon=True)
t1.start()
