import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.transform.scale(pg.image.load("../assets/ralph.png"), (40, 70))
        self.rect = self.image.get_rect()

        self.movex = 0
        self.movey = 0

        self.rect.center = [445, 590]

    def control(self, x, y):
        self.movex += x
        self.movey += y

    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        # print(self.rect.center)
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 894 - 40:
            self.rect.x = 894 - 40
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 570:
            self.rect.y = 570
