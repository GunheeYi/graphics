from time import sleep, time
import numpy as np
import pygame
from math import sin, cos, tan, radians, sqrt

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
    def __str__(self):
        return "({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)
    def __repr__(self):
        return str(self)
    def __add__(self, v):
        if type(v)==V3: return V3(self.x+v.x, self.y+v.y, self.z+v.z)
        raise TypeError
    def __sub__(self, v):
        if type(v)==V3: return self.__add__(-v)
        raise TypeError
    def __mul__(self, v): # dot product
        if type(v)==V3: return self.x * v.x + self.y * v.y + self.z * v.z
        else: return V3(self.x*v, self.y*v, self.z*v)
        # raise TypeError
    def __neg__(self):
        return self.__mul__(-1)
    def __pow__(self, v): # cross product
        if type(v)==V3: return V3(self.y*v.z-self.z*v.y, self.z*v.x-self.x*v.z, self.x*v.y-self.y*v.x)
        raise TypeError
    def __floordiv__(self, denom):
        return V3(self.x/denom, self.y/denom, self.z/denom)
    def __div__(self, denom):
        return self.__floordiv__(denom)
    def len(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    def normed(self):
        return self.__div__(self.len())
    def norm(self):
        self = self.normed()
        return self

class M4x4:
    def __init__(self, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16):
        r1 = [m1, m2, m3, m4]
        r2 = [m5, m6, m7, m8]
        r3 = [m9, m10, m11, m12]
        r4 = [m13, m14, m15, m16]
        self.m = [r1, r2, r3, r4]
    def __mul__(self, a):
        if type(a)==V3:
            x = self.m[0][0]*a.x + self.m[0][1]*a.y + self.m[0][2]*a.z + self.m[0][3]
            y = self.m[1][0]*a.x + self.m[1][1]*a.y + self.m[1][2]*a.z + self.m[1][3]
            z = self.m[2][0]*a.x + self.m[2][1]*a.y + self.m[2][2]*a.z + self.m[2][3]
            w = self.m[3][0]*a.x + self.m[3][1]*a.y + self.m[3][2]*a.z + self.m[3][3]
            return V3(x/w, y/w, z/w)
        elif type(a)==M4x4:
            return M4x4(
                self.m[0][0]*a.m[0][0] + self.m[0][1]*a.m[1][0] + self.m[0][2]*a.m[2][0] + self.m[0][3]*a.m[3][0],
                self.m[0][0]*a.m[0][1] + self.m[0][1]*a.m[1][1] + self.m[0][2]*a.m[2][1] + self.m[0][3]*a.m[3][1],
                self.m[0][0]*a.m[0][2] + self.m[0][1]*a.m[1][2] + self.m[0][2]*a.m[2][2] + self.m[0][3]*a.m[3][2],
                self.m[0][0]*a.m[0][3] + self.m[0][1]*a.m[1][3] + self.m[0][2]*a.m[2][3] + self.m[0][3]*a.m[3][3],
                self.m[1][0]*a.m[0][0] + self.m[1][1]*a.m[1][0] + self.m[1][2]*a.m[2][0] + self.m[1][3]*a.m[3][0],
                self.m[1][0]*a.m[0][1] + self.m[1][1]*a.m[1][1] + self.m[1][2]*a.m[2][1] + self.m[1][3]*a.m[3][1],
                self.m[1][0]*a.m[0][2] + self.m[1][1]*a.m[1][2] + self.m[1][2]*a.m[2][2] + self.m[1][3]*a.m[3][2],
                self.m[1][0]*a.m[0][3] + self.m[1][1]*a.m[1][3] + self.m[1][2]*a.m[2][3] + self.m[1][3]*a.m[3][3],
                self.m[2][0]*a.m[0][0] + self.m[2][1]*a.m[1][0] + self.m[2][2]*a.m[2][0] + self.m[2][3]*a.m[3][0],
                self.m[2][0]*a.m[0][1] + self.m[2][1]*a.m[1][1] + self.m[2][2]*a.m[2][1] + self.m[2][3]*a.m[3][1],
                self.m[2][0]*a.m[0][2] + self.m[2][1]*a.m[1][2] + self.m[2][2]*a.m[2][2] + self.m[2][3]*a.m[3][2],
                self.m[2][0]*a.m[0][3] + self.m[2][1]*a.m[1][3] + self.m[2][2]*a.m[2][3] + self.m[2][3]*a.m[3][3],
                self.m[3][0]*a.m[0][0] + self.m[3][1]*a.m[1][0] + self.m[3][2]*a.m[2][0] + self.m[3][3]*a.m[3][0],
                self.m[3][0]*a.m[0][1] + self.m[3][1]*a.m[1][1] + self.m[3][2]*a.m[2][1] + self.m[3][3]*a.m[3][1],
                self.m[3][0]*a.m[0][2] + self.m[3][1]*a.m[1][2] + self.m[3][2]*a.m[2][2] + self.m[3][3]*a.m[3][2],
                self.m[3][0]*a.m[0][3] + self.m[3][1]*a.m[1][3] + self.m[3][2]*a.m[2][3] + self.m[3][3]*a.m[3][3]
            )
        else: raise TypeError
    def t(self):
        return M4x4(
            self.m[0][0], self.m[1][0], self.m[2][0], self.m[3][0],
            self.m[0][1], self.m[1][1], self.m[2][1], self.m[3][1],
            self.m[0][2], self.m[1][2], self.m[2][2], self.m[3][2],
            self.m[0][3], self.m[1][3], self.m[2][3], self.m[3][3]
        )
    def I():
        return M4x4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)

class Triangle:
    def __init__(self, p0, p1, p2):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
    def transformed(self, m):
        return Triangle(m*self.p0, m*self.p1, m*self.p2)
    def transform(self, m):
        self = self.transformed(m)
        return self
    def __str__(self):
        return "Triangle: {}, {}, {}".format(self.p0, self.p1, self.p2)
    def __repr__(self):
        return str(self)

class Mesh:
    def __init__(self, l):
        self.l = l
    def transformed(self, m):
        return Mesh(list(map(lambda _: _.transformed(m), self.l)))
    def transform(self, m):
        self = self.transformed(m)
        return self
    def __str__(self):
        s = "Mesh:"
        for el in self.l:
            s += "\n\t{}".format(el)
        return s
    def __repr__(self):
        return str(self)

cube = Mesh([
    Triangle(V3(0,0,0), V3(1,0,0), V3(0,0,1)), Triangle(V3(1,0,0), V3(1,0,1), V3(0,0,1)), # front
    Triangle(V3(1,0,0), V3(1,1,0), V3(1,0,1)), Triangle(V3(1,0,1), V3(1,1,0), V3(1,1,1)), # right
    Triangle(V3(1,1,1), V3(1,1,0), V3(0,1,0)), Triangle(V3(0,1,0), V3(0,1,1), V3(1,1,1)), # back
    Triangle(V3(0,0,1), V3(0,1,1), V3(0,0,0)), Triangle(V3(0,0,0), V3(0,1,1), V3(0,1,0)), # left
    Triangle(V3(0,1,1), V3(0,0,1), V3(1,1,1)), Triangle(V3(1,1,1), V3(0,0,1), V3(1,0,1)), # top
    Triangle(V3(0,0,0), V3(0,1,0), V3(1,1,0)), Triangle(V3(1,1,0), V3(1,0,0), V3(0,0,0)), # bottom
])

class World:
    def __init__(self, dimension, title="New Window"):
        self.objs = list()
        self.w, self.h = dimension[0], dimension[1]
        pygame.init()
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption(title)
        self.canvas = np.full((self.w, self.h, 3), 255.0)
        self.cam = V3(5, 5, 5)
        self.forward = V3(-1, -1, -1).normed()
        self.upward = V3(-0.5, -0.5, 1).normed()
        self.runningg = True
        self.start = time()
    def add(self, obj):
        self.objs.append(obj)
    def clear(self):
        self.canvas = np.full((self.w, self.h, 3), 255.0)
    def setPixel(self, x, y, rgb=BLACK):
        x, y = round(x), round(y)
        if x >= 0 and x < self.w and y >= 0 and y < self.h: self.canvas[x, self.h-1-y, :] = np.array([rgb.r, rgb.g, rgb.b])
    def drawRow(self, x1, x2, y, rgb=BLACK):
        for x in range(x1, x2+1):
            self.setPixel(x, y, rgb)
    def drawCol(self, x, y1, y2, rgb=BLACK):
        for y in range(y1, y2+1):
            self.setPixel(x, y, rgb)
    def drawLine(self, x1, y1, x2, y2, rgb=BLACK):
        x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)
        # fill a vertical/horizontal line if given so
        if x1==x2:
            self.drawCol(x1, y1, y2, rgb)
            return
        if y1==y2:
            self.drawRow(x1, x2, y1, rgb)
            return
        xRange, yRange = x2-x1, y2-y1
        if abs(xRange) >= abs(yRange):
            for x in range(min(x1,x2), max(x1,x2)+1):
                y = y1 + yRange * (x-x1) / xRange
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        self.setPixel(x+dx,y+dy,rgb)
        else:
            for y in range(min(y1,y2), max(y1,y2)+1):
                x = x1 + xRange * (y-y1) / yRange
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        self.setPixel(x+dx,y+dy,rgb)
    def draw(self, obj):
        rgb = BLACK
        if type(obj)==Triangle:
            self.drawLine(obj.p0.x, obj.p0.y, obj.p1.x, obj.p1.y, rgb)
            self.drawLine(obj.p1.x, obj.p1.y, obj.p2.x, obj.p2.y, rgb)
            self.drawLine(obj.p2.x, obj.p2.y, obj.p0.x, obj.p0.y, rgb)
        elif type(obj)==Mesh:
            for el in obj.l:
                self.draw(el)
        
    def running(self): return self.runningg
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runningg = False
                return
        self.clear()
        t = (time() - self.start) % 3
        self.cam = V3(t, t, t)
        translate = M4x4(1, 0, 0, -self.cam.x, 0, 1, 0, -self.cam.y, 0, 0, 1, -self.cam.z, 0, 0, 0, 1)
        camZ, camY = -self.forward, self.upward
        camX = camY**camZ
        align = M4x4(camX.x, camX.y, camX.z, 0, camY.x, camY.y, camY.z, 0, camZ.x, camZ.y, camZ.z, 0, 0, 0, 0, 1).t()
        toScreen = M4x4(100, 0, 0, self.w/2, 0, 100, 0, self.h/2, 0, 0, 1, 0, 0, 0, -1, 1)
        vertexShader = toScreen * align * translate
        # vertexShader = toScreen * align
        for obj in self.objs:
            # print(obj)
            obj_transformed = obj.transformed(vertexShader)
            print(obj_transformed)
            self.draw(obj_transformed)
        surf = pygame.surfarray.make_surface(self.canvas.astype('uint8'))
        self.display.blit(surf, (0, 0))
        pygame.display.update()
    def quit(self):
        pygame.quit()

world = World((700, 400), "Homemade Graphics Engine!")
world.add(cube)
while world.running():
    world.update()
world.quit()