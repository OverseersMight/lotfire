import pygame as pg


class Fire(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.sprites = []
        self.sprites.append(pg.image.load('../assets/Fire/fire_0.png'))
        self.sprites.append(pg.image.load('../assets/Fire/fire_1.png'))
        self.sprites.append(pg.image.load('../assets/Fire/fire_2.png'))
        self.sprites.append(pg.image.load('../assets/Fire/fire_3.png'))
        self.sprites.append(pg.image.load('../assets/Fire/fire_4.png'))
        self.sprites.append(pg.image.load('../assets/Fire/fire_5.png'))
        self.sprites.append(pg.image.load('../assets/Fire/fire_6.png'))

        self.current_sprite = 0
        self.image = pg.transform.scale(self.sprites[self.current_sprite], (180, 180))
        self.rect = self.image.get_rect()

        self.rect.center = [435, 230]

    def update(self):
        self.current_sprite += 0.1

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.rect = self.image.get_rect()

        self.rect.center = [435, 230]

        self.image = pg.transform.scale(self.sprites[int(self.current_sprite)], (180, 180))
