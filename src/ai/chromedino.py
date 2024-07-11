# Lib
import random
import pygame
import numpy as np

from game.settings import *

# Object import Cactus, Bird, Cloud
from game.objects.obstacles import generate_obstacles
from game.objects.dinosaur import Dinosaur

# AI
from ai.prediction import next_step

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
def start_game(genomes) -> list[tuple]:
    clock = pygame.time.Clock()
        
    players = [Dinosaur() for _ in genomes]
    game = Game()

    fitnesses: list[tuple] = []

    while True:
        SCREEN.fill(BACKGROUND_COLOR)

        # Progress
        game.distance += game.speed

        if game.distance - game.points * 50 > 50:
            game.points += 1
        if game.distance - game.speed * 700 > 700:
            game.speed += 1
        
        # Obstacle generation
        if game.distance > game.next_generate_distance:
            generate_obstacles(game.obstacles)
            game.next_generate_distance += random.randint(450, 900)
        
        genomes_copy = genomes.copy()

        # Prediction
        for i, player in enumerate(players.copy()):
            if game.obstacles:
                move = next_step(
                    genomes_copy[i],
                    np.array([
                        game.speed,
                        player.rect.y,
                        game.obstacles[0].rect.x,
                        game.obstacles[0].rect.y
                ]))
            else:
                move = 1

            if move == 1:
                player.is_ducked = False
                player.is_running = False
                player.is_jumping = True
            elif not player.is_jumping:
                player.is_ducked = False
                player.is_running = True

            player.update()

            # Update, drawing and collision
            for obstacle in game.obstacles.copy():
                # Collision detection
                # Even works without mask property but slower since it 
                # creates one on the fly from the image attribute.
                if pygame.sprite.collide_mask(player, obstacle):
                    genomes_copy[i].score = game.distance
                    fitnesses.append(genomes_copy[i])
                    players.remove(player)
                    genomes.remove(genomes_copy[i])
                    break
    
        for obstacle in game.obstacles:
            obstacle.update(game.speed, game.obstacles)
            obstacle.draw(SCREEN)

        if players == []:
            return fitnesses
        
        players[0].draw(SCREEN)
        
        pygame.display.update()
        clock.tick(FRAME_RATE)
