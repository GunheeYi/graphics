from time import sleep, time

class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

WIDTH, HEIGHT = 100, 30

SCREEN_BASE = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

SCREEN = SCREEN_BASE.copy()

def clear():
    SCREEN = SCREEN_BASE.copy()

def fill(xy):
    SCREEN[HEIGHT-1-xy.y][xy.x] = '▇'

def render(pixels):
    clear()
    for pixel in pixels: fill(pixel)
    output = '\n'.join(''.join(col for col in row) for row in SCREEN)
    print(output)

for i in range(30):
    render([XY(3*i, i)])
    sleep(0.1)
    