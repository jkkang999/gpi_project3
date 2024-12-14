import pygame
import math

def aabb_collision(player_rect, obstacle):
    """
    AABB 충돌 감지: 두 직사각형이 겹치는지 확인
    """
    return (
        player_rect.left < obstacle.right and
        player_rect.right > obstacle.left and
        player_rect.top < obstacle.bottom and
        player_rect.bottom > obstacle.top
    )
