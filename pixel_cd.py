import pygame
import math

def pixel_cd(player_surface, player_rect, obstacle_surface, obstacle_rect):
    """
    픽셀 단위 충돌 감지 함수.
    """
    intersection = player_rect.clip(obstacle_rect)
    if intersection.width == 0 or intersection.height == 0:
        return False

    x1, y1 = intersection.x - player_rect.x, intersection.y - player_rect.y
    x2, y2 = intersection.x - obstacle_rect.x, intersection.y - obstacle_rect.y

    sub_player = player_surface.subsurface((x1, y1, intersection.width, intersection.height))
    sub_obstacle = obstacle_surface.subsurface((x2, y2, intersection.width, intersection.height))

    for y in range(intersection.height):
        for x in range(intersection.width):
            if sub_player.get_at((x, y)).a > 0 and sub_obstacle.get_at((x, y)).a > 0:
                return True

    return False
