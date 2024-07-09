import random

from settings import *


class Cloud:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(160, 190)
        self.slowness = 0.15
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game_speed, prev_cloud):
        self.x -= game_speed * self.slowness
        if self.x < -self.width:
            self.x = prev_cloud.x + random.randint(500, 700)
            self.y = random.randint(80, 130)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))
