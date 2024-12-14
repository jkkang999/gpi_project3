import pygame
import math
import random

# Convex Hull 계산 (Graham's Scan)
def graham_scan(points):
    def ccw(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    points = sorted(points, key=lambda p: (p[1], p[0]))  # y좌표, x좌표 기준 정렬
    start = points[0]
    points = sorted(points, key=lambda p: math.atan2(p[1] - start[1], p[0] - start[0]))

    hull = [start]
    for point in points[1:]:
        while len(hull) > 1 and ccw(hull[-2], hull[-1], point) <= 0:
            hull.pop()  # 시계 방향인 경우 pop
        hull.append(point)
    return hull

# SAT로 충돌 검사
def sat_collision(hull1, hull2):
    def get_axes(hull):
        axes = []
        for i in range(len(hull)):
            p1, p2 = hull[i], hull[(i + 1) % len(hull)]
            edge = (p2[0] - p1[0], p2[1] - p1[1])
            axes.append((-edge[1], edge[0]))  # 법선 벡터 계산
        return axes

    def project(hull, axis):
        dots = [p[0] * axis[0] + p[1] * axis[1] for p in hull]
        return min(dots), max(dots)

    def overlap(proj1, proj2):
        return not (proj1[1] < proj2[0] or proj2[1] < proj1[0])

    axes1 = get_axes(hull1)
    axes2 = get_axes(hull2)

    for axis in axes1 + axes2:
        proj1 = project(hull1, axis)
        proj2 = project(hull2, axis)
        if not overlap(proj1, proj2):
            return False
    return True

# 두 다각형 생성
def generate_random_points(center, num_points=8, radius=50):
    return [(center[0] + random.randint(-radius, radius), center[1] + random.randint(-radius, radius)) for _ in range(num_points)]

# Convex Hull 이동
def move_points(points, dx, dy):
    return [(x + dx, y + dy) for x, y in points]