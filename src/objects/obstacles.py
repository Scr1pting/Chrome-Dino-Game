from settings import *

import pygame # type: ignore
import random


class Obstacle:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)


class SmallCactus(Obstacle):
    def __init__(self, images):
        self.obstacle_type = random.randint(0, 2)
        self.image = images[self.obstacle_type]
        super().__init__(self.image)
        self.rect.y = 328

class LargeCactus(Obstacle):
    def __init__(self, images):
        self.obstacle_type = random.randint(0, 2)
        self.image = images[self.obstacle_type]
        super().__init__(self.image)
        self.rect.y = 303


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, images):
        self.obstacle_type = 0
        self.images = images
        self.image = images[0]
        super().__init__(self.image)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        
        if self.index >= 5:
            self.image = self.images[0]
        else:
            self.image = self.images[1]

        self.mask = pygame.mask.from_surface(self.image)
        
        SCREEN.blit(self.image, self.rect)
        self.index += 1
