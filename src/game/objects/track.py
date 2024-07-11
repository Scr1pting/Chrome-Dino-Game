from game.settings import *


class Track:
    def __init__(self) -> None:
        self.image = TRACK
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 380

    def update(self, game_speed) -> None:
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            self.rect.x = 0

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, self.rect)
        SCREEN.blit(self.image, (self.rect.x + self.rect.width, self.rect.y))
