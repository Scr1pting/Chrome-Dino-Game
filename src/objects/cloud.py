import random

from settings import *


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(50, 100)
        self.z = random.randint(3, 9)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game_speed):
        self.x -= game_speed/self.z
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
            self.z = random.randint(3, 9)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))
