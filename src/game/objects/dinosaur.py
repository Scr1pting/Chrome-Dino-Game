from game.settings import *

import pygame


class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 22
    CYCLE_LENGTH = 12

    def __init__(self):
        self.duck_img = DUCKING
        self.run_imgs = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DEAD

        self.run_masks = [pygame.mask.from_surface(img) for img in RUNNING]
        self.jump_mask = pygame.mask.from_surface(JUMPING)
        self.duck_masks = [pygame.mask.from_surface(img) for img in DUCKING]

        self.is_ducked = False
        self.is_running = True
        self.is_jumping = False
        self.is_dead = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL

        self.image = self.run_imgs[0]
        self.mask = self.run_masks[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS


    def update(self):
        # Executing states
        if self.is_ducked:
            self.duck()
        if self.is_running:
            self.run()
        if self.is_jumping:
            self.jump()
        # Step cycle 
        if self.step_index >= self.CYCLE_LENGTH:
            self.step_index = 0
        # Get the input of user
        user_input = pygame.key.get_pressed()
        
        # If block for setting the states
        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.is_jumping:
            self.is_ducked = False
            self.is_running = False
            self.is_jumping = True
        elif user_input[pygame.K_DOWN] and not self.is_jumping:
            self.is_ducked = True
            self.is_running = False
            self.is_jumping = False
        elif not (self.is_jumping or user_input[pygame.K_DOWN]):
            self.is_ducked = False
            self.is_running = True
            self.is_jumping = False

    def duck(self):
        current_index = self.step_index // (self.CYCLE_LENGTH // 2)

        self.image = self.duck_img[current_index]
        self.mask = self.duck_masks[current_index]

        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCK

        self.step_index += 1

    def run(self):
        current_index = self.step_index // (self.CYCLE_LENGTH // 2)

        self.image = self.run_imgs[current_index]
        self.mask = self.run_masks[current_index]

        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS

        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        self.mask = self.jump_mask        
        self.rect.y -= int(self.jump_vel)
        self.jump_vel -= 1.45
        # When landing, the dinosaur has the same velocity as at
        # starting position, just in opposite direction.
        if self.jump_vel < -self.JUMP_VEL:
            self.is_jumping = False
            self.jump_vel = self.JUMP_VEL
            self.rect.y = self.Y_POS

    def dead(self):
        self.is_dead = True
        self.image = self.dead_img
        self.rect.x = self.X_POS
        # When ducking
        if self.rect.y > self.Y_POS:
            self.rect.y = self.Y_POS

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
