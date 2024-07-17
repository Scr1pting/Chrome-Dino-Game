# Lib
import random
import threading
import pygame

from game.game_logic import Game, get_game_speed
from game.settings import *
from game.menus import initial_screen, restart_screen
from game.scoring import load_highscore, draw_score

# Object import Cactus, Bird, Cloud
from game.objects.obstacles import generate_obstacles
from game.objects.dinosaur import Dinosaur
from game.objects.cloud import Cloud, draw_clouds
from game.objects.track import Track

# Init
pygame.init()


# MARK: Main
def start_game():
    clock = pygame.time.Clock()

    player = Dinosaur()
    track = Track()
    clouds = [Cloud(x=600*i) for i in range(2)]
    
    highscore = load_highscore()
    initial_screen(highscore)

    game = Game()

    while True:
        SCREEN.fill(BACKGROUND_COLOR)

        # Background
        track.update(game.speed)
        track.draw(SCREEN)

        draw_clouds(clouds, game.speed)

        # Get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Progress
        game.distance += game.speed
        game.frame += 1

        if game.distance - game.points * 50 > 50:
            game.points += 1
        game.speed = get_game_speed(game.distance)

        # Update score display
        draw_score(highscore, game.points)
        
        # Obstacle generation
        if game.distance > game.next_generate_distance:
            generate_obstacles(game.obstacles)
            game.next_generate_distance += random.randint(500, 1000)
        
        # Update, drawing and collision
        for obstacle in game.obstacles:
            # Draw call
            obstacle.update(game.speed, game.obstacles)
            obstacle.draw(SCREEN)
        
        # Collision detection
        # Even works without mask property but slower since it 
        # creates one on the fly from the image attribute.
        # Other obstacles are not rendered because loop is broken
        # before.
        if pygame.sprite.collide_mask(player, game.obstacles[0]):
            player.dead()
            player.draw(SCREEN)
            pygame.display.update()
            break
        else:
            # Player
            player.update()
            player.draw(SCREEN)

        # Death
        if player.is_dead: 
            restart_screen()

            while player.is_dead:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        game = Game()
                        player.is_dead = False
                        break
        
        pygame.display.update()
        clock.tick(FRAME_RATE)


if __name__ == "__main__":
    # Start thread
    t1 = threading.Thread(target=start_game(), daemon=True)
    t1.start()
