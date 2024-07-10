# Lib
import random
import pygame
import numpy as np

from game.settings import *

# Object import Cactus, Bird, Cloud
from game.objects.obstacles import generate_obstacles
from game.objects.dinosaur import Dinosaur

# Evolutionary algorithm
from evo import Genome, next_step

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


# MARK: Main
def start_game(genome: Genome) -> int:
    player = Dinosaur()
    game = Game()

    while True:
        SCREEN.fill(BACKGROUND_COLOR)

        # Progress
        game.distance += game.speed

        if game.distance % 50 == 0:
            game.points += 1
        if game.distance % 700 == 0:
            game.speed += 1
        
        # Obstacle generation
        if game.distance > game.next_generate_distance:
            generate_obstacles(game.obstacles)
            game.next_generate_distance += random.randint(450, 900)
        
        # Prediction
        move = next_step(
            genome,
            np.array([
                game.speed,
                player.rect.y,
                game.obstacles[0].rect.x,
                game.obstacles[0].rect.y
            ])
        )

        if move == 0:
            player.duck()
        elif move == 1:
            player.run()
        elif move == 2:
            player.jump()

        # Update, drawing and collision
        for obstacle in game.obstacles.copy():
            # Draw call
            obstacle.update(game.speed, game.obstacles)

            # Collision detection
            # Even works without mask property but slower since it 
            # creates one on the fly from the image attribute.
            if pygame.sprite.collide_mask(player, obstacle):
                return game.points
