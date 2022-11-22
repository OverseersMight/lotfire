import pygame as pg
import random
import math


class Beast(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.transform.scale(pg.image.load("../assets/beast.png"), (110, 102))
        self.rect = self.image.get_rect()
        self.rect.x = 445
        self.rect.y = 10

        self.movex = 0
        self.movey = 0
        self.dir = 0
        self.rect.topleft = [random.randint(0, 894), random.randint(0, 570)]

    def calc(self, px, py, speed):
        dx = px - self.rect.x
        dy = py - self.rect.y

        if dx < 0 and self.dir == 1:
            self.image = pg.transform.flip(self.image, True, False)
            self.dir = 0
        elif dx > 0 and self.dir == 0:
            self.image = pg.transform.flip(self.image, True, False)
            self.dir = 1

        dist = math.hypot(dx, dy)

        if dist == 0:
            return False

        self.movex = min(speed, dist) * dx / dist
        self.movey = min(speed, dist) * dy / dist

        return True

    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 894 - 50:
            self.rect.x = 894 - 50
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 570:
            self.rect.y = 570