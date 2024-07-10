from settings import *
from objects.cloud import Cloud

def draw_ground(x_pos_bg: int, y_pos_bg: int, game_speed: int):
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    
    if x_pos_bg <= -image_width:
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg = 0
    
    x_pos_bg -= game_speed
    return x_pos_bg

def draw_clouds(clouds: list[Cloud], game_speed: int):
    for index, cloud in enumerate(clouds):
        prev_cloud = clouds[index - 1]
        cloud.update(game_speed, prev_cloud)
        cloud.draw(SCREEN)
