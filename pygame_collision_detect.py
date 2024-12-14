import pygame
import sys
import math
import Sphere_cd
import AABB_cd
import OBB_cd
import Convex_Hull_cd
import pixel_cd

# Initialize pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Collision Detection Methods")

# Load player image
player_image = pygame.image.load("player.png")  # Replace with your player image path
player_rect = player_image.get_rect(center=(screen_width // 2 - 100, screen_height // 2))

# Player's floating position
player_pos = pygame.Vector2(player_rect.x, player_rect.y)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DEFAULT_BACKGROUND = WHITE
COLLISION_BACKGROUND = (255, 200, 200)  # Light red for collision

# Font for displaying text
font = pygame.font.Font(None, 36)

# Rectangular obstacle for AABB
obstacle = pygame.Rect(500, 200, 100, 200)

# 중심과 OBB 크기
obb_center = [550, 300]
obb_size = [100, 200]  # width, height
obb_angle = 0  # 초기 각도 (도 단위)

# Movement speed
player_speed = 0.5

# pixel_collision의 초기 각도 (도 단위)
pixel_angle = 0

# Game loop
running = True
collision_mode = 1  # 1: Sphere, 2: AABB, 3: OBB
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                collision_mode = 1
            elif event.key == pygame.K_2:
                collision_mode = 2
            elif event.key == pygame.K_3:
                collision_mode = 3
            elif event.key == pygame.K_4:
                collision_mode = 4
            elif event.key == pygame.K_5:
                collision_mode = 5

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= player_speed
    if keys[pygame.K_s]:
        player_pos.y += player_speed
    if keys[pygame.K_a]:
        player_pos.x -= player_speed
    if keys[pygame.K_d]:
        player_pos.x += player_speed

    # Update player_rect position with the floating coordinates
    player_rect.x, player_rect.y = int(player_pos.x), int(player_pos.y)

#########################################################################################################

    # Collision detection
    collision = False

    if collision_mode == 1:
        obstacle_center = (obstacle.x + obstacle.width // 2, obstacle.y + obstacle.height // 2)
        collision = Sphere_cd.sphere_collision(player_rect, obstacle_center, obstacle.width // 2)
        text = "Sphere Collision Detection"

    elif collision_mode == 2:
        collision = AABB_cd.aabb_collision(player_rect, obstacle)
        text = "AABB Collision Detection"

    elif collision_mode == 3:
        # OBB: Draw the rectangular obstacle (same as AABB for simplicity here)
        detection_rect = OBB_cd.draw_obb(screen, player_rect.center, [49,77], 20, BLUE)  # Expand the rectangle by 20 pixels in all directions
        # OBB 그리기
        obb_points = OBB_cd.draw_obb(screen, obb_center, obb_size, obb_angle, RED)
        collision = OBB_cd.check_collision(detection_rect, obb_points)
        text = "OBB Collision Detection"
    
    elif collision_mode == 4:
        points1 = [(player_rect.x + 22, player_rect.y + 16),
                    (player_rect.x + 45, player_rect.y + 0),
                    (player_rect.x + 50, player_rect.y + 0),
                    (player_rect.x + 55, player_rect.y + 3),
                    (player_rect.x + 65, player_rect.y + 19),
                    (player_rect.x + 41, player_rect.y + 74),
                    (player_rect.x + 2, player_rect.y + 57),
                    (player_rect.x + 2, player_rect.y + 52),
                    ]
        points2 = [(obstacle.x, obstacle.y),(obstacle.x + obstacle.width, obstacle.y),(obstacle.x, obstacle.y + obstacle.height),(obstacle.x + obstacle.width, obstacle.y + obstacle.height)]
        hull1 = Convex_Hull_cd.graham_scan(points1)
        hull2 = Convex_Hull_cd.graham_scan(points2)
        # 충돌 여부 확인
        collision = Convex_Hull_cd.sat_collision(hull1, hull2)
        text = "Convex Hull Collision Detection"
    
    elif collision_mode == 5:
        obstacle_surface = pygame.Surface(obstacle.size, pygame.SRCALPHA)
        pygame.draw.rect(obstacle_surface, RED, (0, 0, *obstacle.size))
        rotated_obstacle_surface = pygame.transform.rotate(obstacle_surface, pixel_angle)
        rotated_obstacle_rect = rotated_obstacle_surface.get_rect(center=obstacle.center)
        collision = pixel_cd.pixel_cd(player_image, player_rect, rotated_obstacle_surface, rotated_obstacle_rect)
        text = "Pixel Collision Detection"
        
#########################################################################################################

    # Change background color based on collision
    if collision:
        background_color = COLLISION_BACKGROUND
    else:
        background_color = DEFAULT_BACKGROUND

    # Clear screen with the selected background color
    screen.fill(background_color)

    # Draw player and obstacle
    screen.blit(player_image, player_rect)
    
#########################################################################################################
    
    if collision_mode == 1:
        # Sphere: Draw a detection circle around the player
        pygame.draw.circle(screen, BLUE, player_rect.center, player_rect.height // 2, 2)
        # Draw the circular obstacle
        pygame.draw.circle(screen, RED, obstacle.center, obstacle.width // 2, 2)

    elif collision_mode == 2:
        # AABB: Draw a detection rectangle around the player
        detection_rect = player_rect  # Expand the rectangle by 20 pixels in all directions
        pygame.draw.rect(screen, BLUE, detection_rect, 2)
        # Draw the rectangular obstacle
        pygame.draw.rect(screen, RED, obstacle, 2)

    elif collision_mode == 3:
        # OBB: Draw the rectangular obstacle (same as AABB for simplicity here)
        detection_rect = OBB_cd.draw_obb(screen, player_rect.center, [49,77], 20, BLUE)  # Expand the rectangle by 20 pixels in all directions
        # OBB 그리기
        obb_points = OBB_cd.draw_obb(screen, obb_center, obb_size, obb_angle, RED)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                        obb_angle -= 2
                elif event.key == pygame.K_e:
                        obb_angle += 2

    elif collision_mode == 4:
        # Convex Hull 그리기
        def draw_hull(points, hull, color):
            pygame.draw.polygon(screen, color, hull, 2)  # Convex Hull
            for point in points:
                pygame.draw.circle(screen, (0, 0, 0), point, 3)  # 점 표시

        draw_hull(points1, hull1, BLUE)
        draw_hull(points2, hull2, RED)
    
    elif collision_mode == 5:
        screen.blit(player_image, player_rect)
        screen.blit(rotated_obstacle_surface, rotated_obstacle_rect.topleft)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                        pixel_angle += 2
                elif event.key == pygame.K_e:
                        pixel_angle -= 2

#########################################################################################################

    # Display method name
    method_text = font.render(text, True, BLUE)
    screen.blit(method_text, (10, 10))

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
