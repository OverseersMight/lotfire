import os
import random
import sys

import pygame as pg
import pygame.freetype

from src.player import Player
from src.log import Log
from src.fire import Fire
from src.beast import Beast
from src.text import Text

RED = pg.Color('red')
clock = pg.time.Clock()
FPS = 60


def end(world, message, font_big, font_small):
    while True:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == ord('r'):
                    main()

        if "LOSE" in message:
            message_surf, message_rect = font_big.render(message, (255, 0, 0))
        else:
            message_surf, message_rect = font_big.render(message, (0, 255, 0))

        message_rect.x = world.get_width() / 2 - message_rect.width / 2
        message_rect.y = world.get_height() / 2 - message_rect.height / 2

        play_again_surf, play_again_rect = font_small.render('PRESS "R" TO PLAY AGAIN', (255, 255, 255))
        play_again_rect.x = world.get_width() / 2 - play_again_rect.width / 2
        play_again_rect.y = 2 * world.get_height() / 3 - play_again_rect.height / 2

        world.fill((0, 0, 1))
        world.blit(message_surf, message_rect)
        world.blit(play_again_surf, play_again_rect)

        pg.display.flip()


def main():
    pg.init()

    log_count = 0
    fire_log_count = 10
    font_big = pygame.freetype.Font("../assets/font.TTF", 48)
    font_small = pygame.freetype.Font("../assets/font.TTF", 24)

    bg = pg.image.load(os.path.join('../assets', 'bg.png'))
    width, height = bg.get_width(), bg.get_height()

    world = pg.display.set_mode([width, height])

    objects = pg.sprite.Group()
    logs = pg.sprite.Group()
    texts = pg.sprite.Group()

    playerSpeed = 5
    beastSpeed = 4

    beast = Beast()
    player = Player()
    fire = Fire()

    objects.add(fire)
    objects.add(beast)
    objects.add(player)

    tick = 1

    run = True
    while run:
        if tick % 120 == 1:
            l = Log()
            l.move(random.randint(0, 824), random.randint(0, 570))
            logs.add(l)

        if tick % 120 == 0:
            fire_log_count -= 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
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
            end(world, "YOU LOSE", font_big, font_small)

        if tick == 3600:
            end(world, "YOU WIN", font_big, font_small)

        # Updates and Redraw
        world.blit(bg, world.get_rect())
        objects.draw(world)
        objects.update()
        logs.draw(world)
        logs.update()

        log_counter = Text(str(log_count), font_big, (0, 0, 0), width - 30, height - 100)
        fire_counter = Text(str(fire_log_count), font_big, (0, 0, 0), width - 30, height - 150)
        if tick % 60 == 0:
            timer = Text(str(int((3600 - tick) / 60)), font_big, (0, 0, 0), width - 30, height - 200)

        texts.add(fire_counter)
        texts.add(log_counter)
        if tick % 60 == 0:
            texts.add(timer)

        texts.draw(world)
        texts.update()

        texts.remove(log_counter)
        texts.remove(fire_counter)
        if (tick+1) % 60 == 0 and tick != 59:
            texts.remove(timer)
        
        pg.display.flip()
        clock.tick(FPS)
        tick += 1


if __name__ == "__main__":
    main()
