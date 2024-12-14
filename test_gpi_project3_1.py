import pygame
import sys
import math

def pixel_collision(surface1, rect1, surface2, rect2):
    """
    픽셀 단위 충돌 감지 함수.
    """
    intersection = rect1.clip(rect2)
    if intersection.width == 0 or intersection.height == 0:
        return False

    x1, y1 = intersection.x - rect1.x, intersection.y - rect1.y
    x2, y2 = intersection.x - rect2.x, intersection.y - rect2.y

    sub_surface1 = surface1.subsurface((x1, y1, intersection.width, intersection.height))
    sub_surface2 = surface2.subsurface((x2, y2, intersection.width, intersection.height))

    for y in range(intersection.height):
        for x in range(intersection.width):
            if sub_surface1.get_at((x, y)).a > 0 and sub_surface2.get_at((x, y)).a > 0:
                return True

    return False

# 초기화
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Surface 생성
rect_size = (200, 100)
surface1 = pygame.Surface(rect_size, pygame.SRCALPHA)
surface2 = pygame.Surface(rect_size, pygame.SRCALPHA)

# Surface에 그림 그리기
pygame.draw.rect(surface1, (255, 0, 0, 255), (0, 0, *rect_size))  # 빨간색 채운 사각형
pygame.draw.rect(surface2, (0, 0, 255, 255), (0, 0, *rect_size))  # 파란색 채운 사각형

# 위치 초기화
rect1 = surface1.get_rect(center=(screen_width // 2, screen_height // 2))
rect2 = surface2.get_rect(center=(400, 300))

# 회전 각도
angle = 0

# 메인 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키보드 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        angle -= 5
    if keys[pygame.K_e]:
        angle += 5

    # Surface2 회전
    rotated_surface2 = pygame.transform.rotate(surface2, angle)
    rect2 = rotated_surface2.get_rect(center=rect2.center)

    # 충돌 감지
    collision = pixel_collision(surface1, rect1, rotated_surface2, rect2)

    # 화면 업데이트
    screen.fill((0, 0, 0))
    screen.blit(surface1, rect1)
    screen.blit(rotated_surface2, rect2)

    if collision:
        pygame.draw.rect(screen, (255, 255, 0), rect1, 2)  # 충돌 시 노란 테두리
        pygame.draw.rect(screen, (255, 255, 0), rect2, 2)

    pygame.display.flip()
    clock.tick(60)
