import os
import random
import sys

import pygame as pg
import pygame.freetype

from src.player import Player
from src.log import Log
from src.fire import Fire
from src.beast import Beast

RED = pg.Color('red')
clock = pg.time.Clock()
FPS = 60


def end(world, message, font):
    while True:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if "LOSE" in message:
            message_surf, message_rect = font.render(message, (255, 0, 0))
        else:
            message_surf, message_rect = font.render(message, (0, 255, 0))

        message_rect.x = world.get_width() / 2 - message_rect.width / 2
        message_rect.y = world.get_height() / 2 - message_rect.height / 2

        world.fill((0, 0, 1))
        world.blit(message_surf, message_rect)

        pg.display.flip()


def main():
    pg.init()

    log_count = 0
    fire_log_count = 10
    font = pygame.freetype.Font("../assets/font.TTF", 48)

    bg = pg.image.load(os.path.join('../assets', 'bg.png'))
    width, height = bg.get_width(), bg.get_height()

    world = pg.display.set_mode([width, height])

    objects = pg.sprite.Group()
    logs = pg.sprite.Group()

    playerSpeed = 5
    beastSpeed = 4

    beast = Beast()
    player = Player()
    fire = Fire()

    objects.add(fire)
    objects.add(beast)
    objects.add(player)

    tick = 1

    while tick <= 3600:
        if tick % 120 == 1:
            l = Log()
            l.move(random.randint(0, 824), random.randint(0, 570))
            logs.add(l)

        if tick % 120 == 0:
            fire_log_count -= 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == ord('w'):
                    player.control(0, -playerSpeed)
                if event.key == ord('s'):
                    player.control(0, playerSpeed)
                if event.key == ord('a'):
                    player.control(-playerSpeed, 0)
                if event.key == ord('d'):
                    player.control(playerSpeed, 0)
            if event.type == pg.KEYUP:
                if event.key == ord('w'):
                    player.control(0, playerSpeed)
                if event.key == ord('s'):
                    player.control(0, -playerSpeed)
                if event.key == ord('a'):
                    player.control(playerSpeed, 0)
                if event.key == ord('d'):
                    player.control(-playerSpeed, 0)

        beast.calc(player.rect.x, player.rect.y, beastSpeed)

        for log in logs:
            if log.rect.colliderect(player.rect):
                logs.remove(log)
                log_count += 1

        if fire.rect.colliderect(player.rect):
            fire_log_count += log_count
            log_count = 0

        if beast.rect.inflate(-10, -50).colliderect(player.rect) or fire_log_count == 0:
            end(world, "YOU LOSE", font)

        world.blit(bg, world.get_rect())
        objects.draw(world)
        objects.update()
        logs.draw(world)
        logs.update()

        log_font_surf, log_font_rect = font.render(str(log_count), (0, 0, 0))
        log_font_rect.x = width - log_font_rect.width - 30
        log_font_rect.y = height - log_font_rect.height - 150
        world.blit(log_font_surf, log_font_rect)

        fire_font_surf, fire_font_rect = font.render(str(fire_log_count), (0, 0, 0))
        fire_font_rect.x = width - fire_font_rect.width - 30
        fire_font_rect.y = height - fire_font_rect.height - 100
        world.blit(fire_font_surf, fire_font_rect)

        pg.display.flip()
        clock.tick(FPS)
        tick += 1

    end(world, "YOU WIN", font)


if __name__ == "__main__":
    main()