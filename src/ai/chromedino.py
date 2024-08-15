# Lib
import random
import pygame
import numpy as np
import math

from game.settings import *
from game.game_logic import Game, get_game_speed, next_object_distance

# Object import Cactus, Bird, Cloud
from game.objects.obstacles import generate_obstacles
from game.objects.dinosaur import Dinosaur
from game.objects.cloud import Cloud, draw_clouds
from game.objects.track import Track

# AI
from ai.prediction import next_step
from ai.stats import draw_stats

# Init
pygame.init()


class Dinosaur_Agent(Dinosaur):
    def __init__(self, genome) -> None:
        super().__init__()
        self.genome = genome


# MARK: Main
def start_game(genomes, epoch) -> list:
    clock = pygame.time.Clock()
        
    players = [Dinosaur_Agent(genome) for genome in genomes]
    game = Game()

    track = Track()

    fitnesses: list = []

    while True:
        SCREEN.fill(BACKGROUND_COLOR)

        # Background
        track.update(game.speed)
        track.draw(SCREEN)

        draw_stats(
            epoch=epoch,
            individuals=len(players),
            max_distance=max(genomes).score,
            current_distance=game.distance
        )

        # Get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Progress
        game.distance += game.speed
        game.speed = get_game_speed(game.distance)
           
        # Obstacle generation
        if game.distance > game.next_generate_distance:
            generate_obstacles(game.obstacles)
            game.next_generate_distance = next_object_distance(
                game.distance, game.speed
            )
        
        # Prediction
        for player in players.copy():
            if game.obstacles:
                move = next_step(
                    player.genome,
                    np.array([
                        game.speed,
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
                player.genome.score = max(
                    player.genome.score, game.distance
                )
                fitnesses.append(player.genome)
                players.remove(player)
                break

        if players == []:
            return fitnesses
    
        for obstacle in game.obstacles.copy():
            obstacle.update(game.speed, game.obstacles)
            obstacle.draw(SCREEN)
        
        pygame.display.update()
        clock.tick(FRAME_RATE)
