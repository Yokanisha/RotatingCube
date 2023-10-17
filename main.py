import pygame
import numpy as np
import math

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100
circle_pos = [WIDTH/2, HEIGHT/2, 0]

angle = 0


"""
points = []
points.append(np.matrix([-1, -1, 1])) #form (1, 3) (row, column)
points.append(np.matrix([1, -1, 1])) # for calculating we need in form of [[1], [-1], [1]]. We will use the fct reshape
points.append(np.matrix([1, 1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))
"""

arr = np.array([-1, -1, 1,
                1, -1, 1,
                1, 1, 1,
                -1, 1, 1,
                -1, -1, -1,
                1, -1, -1,
                1, 1, -1,
                -1, 1, -1
                ])

points = arr.reshape(8, 3)

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])

projected_points = [
    [n, n] for n in range(len(points))
]

def connect_points(i, j, points):
    pygame.draw.line(screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]), 2)

clock = pygame.time.Clock()
while True:

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: ##change
                pygame.quit()
                exit()

    rotation_z = np.matrix([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])

    rotation_y = np.matrix([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]

    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]

    ])

    angle += 0.01

    screen.fill(WHITE)

    i = 0
    for point in points:
        rotated2d = np.dot(rotation_z, point.reshape(3, 1))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d) # example.: [[0.123], [0.321], [0]]

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, RED, (x, y), 5)
        i += 1

    #lines
    """
    connect_points(0, 1, projected_points)
    connect_points(1, 2, projected_points)
    connect_points(2, 3, projected_points)
    connect_points(3, 0, projected_points)

    connect_points(4, 5, projected_points)
    connect_points(5, 6, projected_points)
    connect_points(6, 7, projected_points)
    connect_points(7, 4, projected_points)

    connect_points(0, 4, projected_points)
    connect_points(1, 5, projected_points)
    connect_points(2, 6, projected_points)
    connect_points(3, 7, projected_points)
    """

    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p + 5) % 4) + 4, projected_points)
        connect_points(p, p+4, projected_points)
    pygame.display.update()

