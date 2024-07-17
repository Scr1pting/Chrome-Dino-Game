from game.settings import *

import pygame
import random


class Obstacle:
    def __init__(self, image):
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)


class SmallCactus(Obstacle):
    def __init__(self):
        self.obstacle_type = random.randint(0, 2)
        self.image = SMALL_CACTUS[self.obstacle_type]
        super().__init__(self.image)
        self.rect.y = 328

class LargeCactus(Obstacle):
    def __init__(self):
        self.obstacle_type = random.randint(0, 2)
        self.image = LARGE_CACTUS[self.obstacle_type]
        super().__init__(self.image)
        self.rect.y = 303


class Bird(Obstacle):
    BIRD_HEIGHTS = [240, 290, 320]

    def __init__(self):
        self.obstacle_type = 0

        self.images = BIRD
        self.image = BIRD[0]

        self.masks = [pygame.mask.from_surface(image) for image in self.images]
        self.mask = self.masks[0]

        super().__init__(self.image)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        CYCLE_LENGTH = 20

        if self.index >= CYCLE_LENGTH:
            self.index = 0
        
        if self.index >= CYCLE_LENGTH // 2:
            self.image = self.images[0]
            self.mask = self.masks[0]
        else:
            self.image = self.images[1]
            self.mask = self.masks[1]
        
        SCREEN.blit(self.image, self.rect)
        self.index += 1


def generate_obstacles(obstacles: list[Obstacle]):
    switch = {
        0: SmallCactus(),
        1: LargeCactus(),
        2: Bird()
    }
    obstacles.append(switch[random.randint(0, 2)])
