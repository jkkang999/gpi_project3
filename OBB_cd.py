import pygame
import math

# OBB 회전 함수
def draw_obb(surface, center, size, angle, color):
    # 각도 변환
    rad_angle = math.radians(angle)
    cos_angle = math.cos(rad_angle)
    sin_angle = math.sin(rad_angle)

    # OBB의 절반 크기
    half_w, half_h = size[0] / 2, size[1] / 2

    # 꼭짓점 계산
    points = [
        (-half_w, -half_h),
        (half_w, -half_h),
        (half_w, half_h),
        (-half_w, half_h),
    ]

    # 회전 및 이동
    rotated_points = []
    for x, y in points:
        rx = x * cos_angle - y * sin_angle + center[0]
        ry = x * sin_angle + y * cos_angle + center[1]
        rotated_points.append((rx, ry))

    # OBB 그리기
    pygame.draw.polygon(surface, color, rotated_points, 2)
    return rotated_points


# 충돌 감지 (SAT 방식)
def check_collision(player_rect, obb_points):

    # 모든 OBB 축 검사
    axes = []
    for i in range(len(obb_points)):
        p1 = obb_points[i]
        p2 = obb_points[(i + 1) % len(obb_points)]
        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0])  # 법선 벡터
        axes.append(normal)

    # 주인공 축 추가
    axes.append((1, 0))
    axes.append((0, 1))

    for axis in axes:
        obb_proj = [project_point(p, axis) for p in obb_points]
        player_proj = [project_point(p, axis) for p in player_rect]
        if max(player_proj) < min(obb_proj) or max(obb_proj) < min(player_proj):
            return False  # 충돌 없음

    return True


# 점을 축에 투영
def project_point(point, axis):
    return (point[0] * axis[0] + point[1] * axis[1]) / (axis[0]**2 + axis[1]**2)