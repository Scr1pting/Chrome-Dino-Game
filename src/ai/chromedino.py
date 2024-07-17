# Lib
import random
import pygame
import numpy as np
import math

from game.settings import *
from game.game_logic import Game, get_game_speed

# Object import Cactus, Bird, Cloud
from game.objects.obstacles import generate_obstacles
from game.objects.dinosaur import Dinosaur

# AI
from ai.prediction import next_step

# Init
pygame.init()


class Dinosaur_Agent(Dinosaur):
    def __init__(self, genome) -> None:
        super().__init__()
        self.genome = genome


# MARK: Main
def start_game(genomes) -> list:
    clock = pygame.time.Clock()
        
    players = [Dinosaur_Agent(genome) for genome in genomes]
    game = Game()

    fitnesses: list = []

    while True:
        SCREEN.fill(BACKGROUND_COLOR)

        # Get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Progress
        game.distance += game.speed

        if game.distance - game.points * 50 > 50:
            game.points += 1
        game.speed = get_game_speed(game.distance)
        
        # Obstacle generation
        if game.distance > game.next_generate_distance:
            generate_obstacles(game.obstacles)
            game.next_generate_distance += random.randint(500, 1000)
        
        # Prediction
        for player in players:
            if game.obstacles:
                move = next_step(
                    player.genome,
                    np.array([
                        game.speed,
                        player.rect.y,
                        game.obstacles[0].rect.x,
                        game.obstacles[0].rect.y
                ]))
            else:
                move = 0

            if move == 1:
                player.is_ducked = False
                player.is_running = False
                player.is_jumping = True
            elif move == 2:
                player.is_ducked = True
                player.is_running = False
                player.is_jumping = False
            elif not player.is_jumping:
                player.is_ducked = False
                player.is_running = True

            player.update()
            player.draw(SCREEN)

            # Collision detection
            # Even works without mask property but slower since it 
            # creates one on the fly from the image attribute.
            if pygame.sprite.collide_mask(player, game.obstacles[0]):
                player.genome.score = game.distance
                fitnesses.append(player.genome)
                players.remove(player)
                break

        if players == []:
            return fitnesses
    
        for obstacle in game.obstacles:
            obstacle.update(game.speed, game.obstacles)
            obstacle.draw(SCREEN)
        
        pygame.display.update()
        clock.tick(FRAME_RATE)
