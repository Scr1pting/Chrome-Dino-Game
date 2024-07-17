import random

from game.settings import *


class Cloud:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(160, 190)
        self.slowness = 0.2
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game_speed, prev_cloud):
        self.x -= game_speed * self.slowness
        if self.x < -self.width:
            self.x = prev_cloud.x + random.randint(500, 700)
            self.y = random.randint(80, 130)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


def draw_clouds(clouds: list[Cloud], game_speed: int):
    for index, cloud in enumerate(clouds):
        prev_cloud = clouds[index - 1]
        cloud.update(game_speed, prev_cloud)
        cloud.draw(SCREEN)
