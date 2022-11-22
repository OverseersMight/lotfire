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


def end(world, message, font_big, font_small, difficulty):
    while True:
        pg.time.delay(100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == ord('r'):
                    main(difficulty)
                if event.key == ord('c'):
                    changeDifficulty(world, font_big, font_small)

        if "LOSE" in message:
            message_surf, message_rect = font_big.render(message, (255, 0, 0))
        else:
            message_surf, message_rect = font_big.render(message, (0, 255, 0))

        message_rect.x = world.get_width() / 2 - message_rect.width / 2
        message_rect.y = world.get_height() / 2 - message_rect.height / 2

        play_again_surf, play_again_rect = font_small.render('PRESS "R" TO PLAY AGAIN', (255, 255, 255))
        play_again_rect.x = world.get_width() / 2 - play_again_rect.width / 2
        play_again_rect.y = 3 * world.get_height() / 4 - play_again_rect.height / 2

        difficulty_surf, difficulty_rect = font_small.render('PRESS "C" TO CHANGE DIFFICULTY', (255, 255, 255))
        difficulty_rect.x = world.get_width() / 2 - difficulty_rect.width / 2
        difficulty_rect.y = 4 * world.get_height() / 5 - difficulty_rect.height / 2

        world.fill((0, 0, 1))
        world.blit(message_surf, message_rect)
        world.blit(play_again_surf, play_again_rect)
        world.blit(difficulty_surf, difficulty_rect)

        pg.display.flip()


def changeDifficulty(world, font_big, font_small):
    difficulty = 1
    while True:
        pg.time.delay(100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == ord('e'):
                    difficulty = 1
                if event.key == ord('m'):
                    difficulty = 2
                if event.key == ord('h'):
                    difficulty = 3
                if event.key == ord('r'):
                    main(difficulty)

        title_surf, title_rect = font_big.render('LORD OF THE FIRE', (255, 0, 0))
        title_rect.x = world.get_width() / 2 - title_rect.width / 2
        title_rect.y = world.get_height() / 3 - title_rect.height / 2

        author_surf, author_rect = font_small.render("BY AIDEN FARLEY, SIMON XU, BOWEN YANG", (255, 255, 255))
        author_rect.x = world.get_width() / 2 - author_rect.width / 2
        author_rect.y = 3 * world.get_height() / 7 - author_rect.height / 2

        start_surf, start_rect = font_small.render('PRESS "R" TO START', (255, 255, 255))
        start_rect.x = world.get_width() / 2 - start_rect.width / 2
        start_rect.y = 3 * world.get_height() / 4 - start_rect.height / 2

        difficulty_surf, difficulty_rect = font_small.render('"E" - EASY  "M" - MEDIUM  "H" - HARD', (255, 255, 255))
        difficulty_rect.x = world.get_width() / 2 - difficulty_rect.width / 2
        difficulty_rect.y = 4 * world.get_height() / 5 - difficulty_rect.height / 2

        world.fill((0, 0, 1))
        world.blit(title_surf, title_rect)
        world.blit(author_surf, author_rect)
        world.blit(difficulty_surf, difficulty_rect)
        world.blit(start_surf, start_rect)

        pg.display.flip()


def main(difficulty):
    pg.init()

    log_decay_rate = 120
    log_count = 0
    fire_log_count = 10
    font_big = pg.freetype.Font("../assets/font.TTF", 48)
    font_small = pg.freetype.Font("../assets/font.TTF", 24)

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

    if difficulty == 1:
        beastSpeed = 3
        log_decay_rate = 120
    if difficulty == 2:
        beastSpeed = 4
        log_decay_rate = 100
    if difficulty == 3:
        playerSpeed = 6
        beastSpeed = 5
        log_decay_rate = 100

    tick = 1

    run = True
    while run:
        if tick % 120 == 1:
            l = Log()
            l.move(random.randint(0, 824), random.randint(0, 570))
            logs.add(l)

        if tick % log_decay_rate == 0:
            fire_log_count -= 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
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
            end(world, "YOU LOSE", font_big, font_small, difficulty)

        if tick == 3600:
            end(world, "YOU WIN", font_big, font_small, difficulty)

        # Updates and Redraw
        world.blit(bg, world.get_rect())
        objects.draw(world)
        objects.update()
        logs.draw(world)
        logs.update()

        log_counter = Text(str(log_count), font_big, (0, 0, 0), width - 30, height - 100)
        fire_counter = Text(str(fire_log_count), font_big, (0, 0, 0), width - 30, height - 150)

        texts.add(fire_counter)
        texts.add(log_counter)

        texts.draw(world)
        texts.update()

        texts.remove(log_counter)
        texts.remove(fire_counter)

        pg.display.flip()
        clock.tick(FPS)
        tick += 1


if __name__ == "__main__":
    main(1)
