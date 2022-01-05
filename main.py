from time import sleep, time
import numpy as np
import pygame
from math import sin, cos, tan, radians

class RGB:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

BLACK = RGB(0, 0, 0)
GRAY = RGB(192, 192, 192)
WHITE = RGB(255, 255, 255)
RED = RGB(255, 0, 0)
GREEN = RGB(0, 255, 0)
BLUE = RGB(0, 0, 255)
CYAN = RGB(0, 255, 255)
MAGENTA = RGB(255, 0, 255)
YELLOW = RGB(255, 255, 0)

class V3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def transform(self, m):
        self = transformed(self, m)
    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

def transformed(old, m):
    x = m[0][0]*old.x + m[0][1]*old.y + m[0][2]*old.z + m[0][3]
    y = m[1][0]*old.x + m[1][1]*old.y + m[1][2]*old.z + m[1][3]
    z = m[2][0]*old.x + m[2][1]*old.y + m[2][2]*old.z + m[2][3]
    w = m[3][0]*old.x + m[3][1]*old.y + m[3][2]*old.z + m[3][3]
    return V3(x/w, y/w, z/w)

class Triangle:
    def __init__(self, p0, p1, p2):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
    def draw(self, rgb=BLACK):
        drawLine(self.p0.x, self.p0.y, self.p1.x, self.p1.y, rgb)
        drawLine(self.p1.x, self.p1.y, self.p2.x, self.p2.y, rgb)
        drawLine(self.p2.x, self.p2.y, self.p0.x, self.p0.y, rgb)
    def transformed(self, m):
        return Triangle(transformed(self.p0, m), transformed(self.p1, m), transformed(self.p2, m))
    def transform(self, m):
        self = self.transformed(m)
    def __str__(self):
        return "Triangle: {}, {}, {}".format(self.p0, self.p1, self.p2)

class Mesh:
    def __init__(self, l):
        self.l = l
    def draw(self):
        for el in self.l: el.draw()
    def transformed(self, m):
        return map(lambda _: _.transformed(), self.l)
    def transform(self, m):
        self = self.transformed(m)

WIDTH, HEIGHT = 500, 500
CANVAS = np.full((WIDTH, HEIGHT, 3), 255.0)

def clear():
    global CANVAS
    CANVAS = np.full((WIDTH, HEIGHT, 3), 255.0)

def setPixel(x, y, rgb=BLACK):
    x, y = round(x), round(y)
    if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT: CANVAS[x, HEIGHT-1-y, :] = np.array([rgb.r, rgb.g, rgb.b])

def drawRow(x1, x2, y, rgb=BLACK):
    for x in range(x1, x2+1):
        setPixel(x, y, rgb)

def drawCol(x, y1, y2, rgb=BLACK):
    for y in range(y1, y2+1):
        setPixel(x, y, rgb)

def drawLine(x1, y1, x2, y2, rgb=BLACK):
    x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)
    # fill a vertical/horizontal line if given so
    if x1==x2: drawCol(x1, y1, y2, rgb)
    if y1==y2: drawRow(x1, x2, y1, rgb)

    xRange, yRange = x2-x1, y2-y1

    if abs(xRange) >= abs(yRange):
        for x in range(min(x1,x2), max(x1,x2)+1):
            y = y1 + yRange * (x-x1) / xRange
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    setPixel(x+dx,y+dy,rgb)
    else:
        for y in range(min(y1,y2), max(y1,y2)+1):
            x = x1 + xRange * (y-y1) / yRange
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    setPixel(x+dx,y+dy,rgb)

pygame.init()
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Homemade Graphics Engine!")

running = True
start = time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clear()
    t = time() - start
    rad = t
    m = [[cos(rad), -sin(rad), 0, 50*t], [sin(rad), cos(rad), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    # m = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]] 
    Triangle(V3(100, 100), V3(200, 300), V3(300, 200)).transformed(m).draw()
    surf = pygame.surfarray.make_surface(CANVAS.astype('uint8'))
    DISPLAY.blit(surf, (0, 0))

    pygame.display.update()
    # sleep(0.1)

pygame.quit()