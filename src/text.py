import pygame as pg


class Text(pg.sprite.Sprite):
    def __init__(self, message, font, color, x_pos, y_pos):
        pg.sprite.Sprite.__init__(self)

        self.image, self.rect = font.render(message, color)

        self.rect.x = x_pos - self.rect.width
        self.rect.y = y_pos - self.rect.height

    def update(self):
        pass
