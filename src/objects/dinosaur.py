from settings import *

import pygame # type: ignore


class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    CYCLE_LENGTH = 12

    def __init__(self):
        self.duck_img = DUCKING
        self.run_imgs = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DEAD

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS


    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= self.CYCLE_LENGTH:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // (self.CYCLE_LENGTH // 2)]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_imgs[self.step_index // (self.CYCLE_LENGTH // 2)]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 2.5
            self.jump_vel -= 0.5
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def dead(self):
        self.image = self.dead_img

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
