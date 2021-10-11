import random
import time
import pygame as pg

pg.init()

screen = pg.display.set_mode((600, 600))
pg.display.set_caption("space invaders (se nao disparar PRESS R)")
bg = pg.transform.scale(pg.image.load("galaxy.png"), (600, 600))
screen.blit(bg, (0, 0))


player_img = pg.image.load('space-invaders.png')
player_x = 270
player_y = 450
pos_player = [player_x, player_y]

enemy_img = pg.image.load('space-ship.png')
enemy_x = random.randint(0, 600-64)
enemy_y = 10
pos_enemy = [enemy_x, enemy_y]

bullet_img = pg.image.load("bullet.png")
bullet_x = player_x + 16
bullet_y = player_y
bullet_state = "ready"
pos_bullet = [bullet_x, bullet_y]

laser_img = pg.image.load("laser.png")
laser_x = enemy_x + 16
laser_y = enemy_y
laser_state = "ready"
pos_laser = [laser_x, laser_y]


def boundaries(pos):
    if pos[1] <= 0:
        pos[1] = 0

    elif pos[0] <= 0:
        pos[0] = 0

    elif pos[1] >= 600 - 64:
        pos[1] = 530

    elif pos[0] >= 600 - 64:
        pos[0] = 540
    return pos


def move(obj, pos):
    screen.blit(obj, pos)


run = True
fps = 60
clock = pg.time.Clock()
lives = 5
score = 0
main_font = pg.font.SysFont("comicsans", 30)
shot = False


def col(pos1, pos2, bol):
    if bol:
        return abs(pos1[0] - pos2[0]) <= 50 and abs(pos1[1] - pos2[1]) <= 50
    else:
        return abs(pos1[0] - pos2[0]) <= 30 and abs(pos1[1] - pos2[1]) <= 30


while run:
    clock.tick(fps)
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for events in pg.event.get():
        if events.type == pg.QUIT:
            run = False
        if events.type == pg.KEYDOWN:
            if events.key == pg.K_UP:
                pos_player[1] -= 20
            if events.key == pg.K_DOWN:
                pos_player[1] += 20
            if events.key == pg.K_RIGHT:
                pos_player[0] += 20
            if events.key == pg.K_LEFT:
                pos_player[0] -= 20
            if events.key == pg.K_SPACE:
                bullet_state = "shot"
            if events.key == pg.K_r:
                bullet_state = "ready"
    pos_enemy[1] += 1

    if laser_state == "ready":
        pos_laser = [pos_enemy[0] + 16, pos_enemy[1]]
        laser_state = "shot"

    if laser_state == "shot":
        screen.blit(laser_img, pos_laser)
        pos_laser[1] += 2.5

        if col(pos_laser, pos_player, False):
            lives -= 1
            laser_state = "ready"
        if pos_laser[1] >= 600 - 32:
            laser_state = "ready"

    if bullet_state == "ready":
        pos_bullet = [pos_player[0] + 16, pos_player[1]]

    if bullet_state == "shot":
        screen.blit(bullet_img, pos_bullet)
        pos_bullet[1] -= 10

        if pos_bullet[1] <= 0:
            pos_bullet = [pos_player[0] + 16, pos_player[1]]
            bullet_state = "ready"

        if col(pos_enemy, pos_bullet, False):
            pos_enemy = [random.randint(0, 600 - 64), 10]
            score += 1
            pos_bullet = [pos_player[0] + 16, pos_player[1]]
            bullet_state = "ready"

    if col(pos_enemy, pos_player, True):
        lives -= 1
        pos_enemy = [random.randint(0, 600 - 64), 10]
    elif pos_enemy[1] >= 600 - 64:
        lives -= 1
        pos_enemy = [random.randint(0, 600 - 64), 10]

    move(enemy_img, pos_enemy)
    move(player_img, boundaries(pos_player))

    lives_label = main_font.render(f"Lives: {lives}", True, (255, 255, 255))
    score_label = main_font.render(f"Score: {score}", True, (255, 255, 255))
    game_label = main_font.render("GAME OVER", True, (255, 255, 255))

    if lives == 0:
        move(game_label, (250, 150))
        run = False

    move(score_label, (600-100, 10))
    move(lives_label, (10, 10))

    pg.display.update()
else:
    time.sleep(2.5)
    print(f"Score: {score}")
