from settings import *
import numpy as np
import pygame # type: ignore
from evo import predict, create_genome


class AiDinosaur:

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
        
        self.genome = create_genome()

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.distance = 0
    def genomeUpdate(self, g):
        self.genome =g

    def update(self, objects, game_speed):
        
        input_values = np.array([float(objects[0].rect.x)/100, float(game_speed)/1000])
        #print((objects[0].rect.x))
        value = predict(self.genome, input_values)
        #print(value)
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= self.CYCLE_LENGTH:
            self.step_index = 0

        if value[1]>value[0]  and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif not self.dino_jump:
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        """
        elif value[2]>value[0] and value[2]>value[1] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        """
        

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
            self.rect.y = self.Y_POS

    def dead(self):
        self.image = self.dead_img
        self.rect.x = self.X_POS
        if self.rect.y > self.Y_POS:
            self.rect.y = self.Y_POS

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        
