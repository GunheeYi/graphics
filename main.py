from time import sleep, time
import numpy as np
import pygame

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

class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Triangle:
    def __init__(self, p1, p2, p3):
        self.ps = [p1, p2, p3]
    def draw(self, rgb=BLACK):
        drawLine(self.ps[0], self.ps[1], rgb)
        drawLine(self.ps[1], self.ps[2], rgb)
        drawLine(self.ps[2], self.ps[0], rgb)

WIDTH, HEIGHT = 500, 500
CANVAS = np.full((WIDTH, HEIGHT, 3), 255.0)

def clear():
    CANVAS = np.full((WIDTH, HEIGHT, 3), 255.0)

def setPixel(xy, rgb=BLACK):
    CANVAS[round(xy.x), HEIGHT-1-round(xy.y), :] = np.array([rgb.r, rgb.g, rgb.b])

def drawRow(x1, x2, y, rgb=BLACK):
    for x in range(x1, x2+1):
        setPixel(x, y, rgb)

def drawCol(x, y1, y2, rgb=BLACK):
    for y in range(y1, y2+1):
        setPixel(x, y, rgb)

def drawLine(xy1, xy2, rgb=BLACK):
    x1, y1 = xy1.x, xy1.y
    x2, y2 = xy2.x, xy2.y

    # fill a vertical/horizontal line if given so
    if x1==x2: drawCol(x1, y1, y2, rgb)
    if y1==y2: drawRow(x1, x2, y1, rgb)

    xRange, yRange = x2-x1, y2-y1

    if abs(xRange) >= abs(yRange):
        for x in range(min(x1,x2), max(x1,x2)+1):
            y = y1 + yRange * (x-x1) / xRange
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    setPixel(XY(x+dx,y+dy),rgb)
    else:
        for y in range(min(y1,y2), max(y1,y2)+1):
            x = x1 + xRange * (y-y1) / yRange
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    setPixel(XY(x+dx,y+dy),rgb)

pygame.init()
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Homemade Graphics Engine!")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Triangle(XY(100, 100), XY(200, 300), XY(300, 200)).draw()
    surf = pygame.surfarray.make_surface(CANVAS.astype('uint8'))
    DISPLAY.blit(surf, (0, 0))

    pygame.display.update()
    sleep(0.1)

pygame.quit()