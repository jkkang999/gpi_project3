import pygame
import math

# Collision detection methods
def sphere_collision(player_rect, obstacle_center, obstacle_radius):
    player_center = player_rect.center
    distance = math.sqrt((player_center[0] - obstacle_center[0])**2 + (player_center[1] - obstacle_center[1])**2)
    return distance < (player_rect.height // 2 + obstacle_radius)