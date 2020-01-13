import pygame
import os
import sys
import random
from pygame import mixer
import time

pygame.init()
mixer.pre_init(44100, -16, 1, 512)
mixer.pre_init(44100, -16, 2, 512)
mixer.init()
soundb = mixer.Sound('data/background music.ogg')
soundis = mixer.Sound('data/impact by sword.ogg')
soundws = mixer.Sound('data/a wave of the sword.ogg')
soundeg = mixer.Sound('data/end game.ogg')
soundgo = mixer.Sound('data/game over.ogg')
soundm = mixer.Sound('data/monster.ogg')
soundrl = mixer.Sound('data/restart the level.ogg')
soundnl = mixer.Sound('data/The sound of going to the next level.ogg')
sounddp = mixer.Sound('data/drinking a potion.ogg')
soundge = mixer.Sound('data/gta_-_mission_compet.ogg')
soundpr = mixer.Sound('data/woman.ogg')
soundco = mixer.Sound('data/chest open.ogg')
size = width, height = 550, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
xp = 100
level_number = 0
turn = 1
flag = 1
point = 0
lvl = ['map1.txt', 'map2.txt', 'map3.txt', 'map4.txt']


def damage(args):
    for sprite in player_group:
        x, y = sprite.rect.center
        for sprite in mob_group:
            if sprite.rect.collidepoint(args) and \
                    (sprite.rect.collidepoint(x - 50, y) or sprite.rect.collidepoint(x + 50, y) or
                     sprite.rect.collidepoint(x, y - 50) or sprite.rect.collidepoint(x, y + 50) or
                     sprite.rect.collidepoint(x - 50, y - 50) or sprite.rect.collidepoint(x + 50, y + 50) or
                     sprite.rect.collidepoint(x - 50, y + 50) or sprite.rect.collidepoint(x + 50, y - 50) or
                     sprite.rect.collidepoint(x, y)):
                soundis.play(0)
                sprite.kill()
                create_particles(pygame.mouse.get_pos())
            else:
                soundws.play(0)


def lava(xp):
    xp = 0
    panel(str(xp), 40, 40, 35)
    return int(xp)


def potion(xp):
    sounddp.play(0)
    if xp > 50:
        xp += (100 - xp)
    else:
        xp += 50
    panel(str(xp), 40, 40, 35)
    return int(xp)


def xxp(xp):
    n = (random.randrange(3) - 1)
    if n == 1:
        xp -= 75
        panel(str(xp), 40, 40, 35)
        return int(xp)
    elif n == 0:
        xp -= 50
        panel(str(xp), 40, 40, 35)
        return int(xp)
    else:
        xp -= 25
        panel(str(xp), 40, 40, 35)
        return int(xp)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def panel(mes, x, y, font_size, font_color=(255, 255, 255), font_type='data/font.ttf'):
    font_size = int(font_size)
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(mes, True, font_color)
    screen.blit(text, (x, y))


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y, a = None, None, None, []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '*':
                Tile('wall2', x, y)
            elif level[y][x] == 'f':
                Tile('floor', x, y)
            elif level[y][x] == 'h':
                Tile('potion', x, y)
            elif level[y][x] == '/':
                Tile('water', x, y)
            elif level[y][x] == '$':
                Tile('princess', x, y)
            elif level[y][x] == '0':
                Tile('stone', x, y)
            elif level[y][x] == '2':
                Tile('stone1', x, y)
            elif level[y][x] == 'L':
                Tile('lava', x, y)
            elif level[y][x] == '%':
                Tile('tree', x, y)
            elif level[y][x] == '3':
                Tile('stone2', x, y)
            elif level[y][x] == 'c':
                Tile('chest', x, y)
            elif level[y][x] == 'g':
                Tile('ground', x, y)
            elif level[y][x] == '1':
                a.append([x, y])
            elif level[y][x] == '!':
                Tile('flag', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                px, py = x, y
                new_player = Player(px, py)
    return new_player, x, y, a


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall' or tile_type == 'stone' or tile_type == 'stone1' or tile_type == 'stone2' or \
                tile_type == 'water' or tile_type == 'wall2' or tile_type == 'tree':
            self.add(walls_group)
        elif tile_type == 'mob':
            self.add(mob_group)
        elif tile_type == 'flag':
            self.add(flag_group)
        elif tile_type == 'potion':
            self.add(potion_group)
        elif tile_type == 'lava':
            self.add(lava_group)
        elif tile_type == 'princess':
            self.add(princess_group)
        elif tile_type == 'chest':
            self.add(chest_group)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(mob_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        y = tile_height * y - 10
        x = tile_width * x
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5, tile_height * pos_y)

    def update(self, *args):
        if turn == 0:
            self.image = pygame.transform.flip(self.image, True, False)
        elif turn == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(tile_width * x + self.rect.x, tile_height * y + self.rect.y)


FPS = 50


class Particle(pygame.sprite.Sprite):
    fire = [(pygame.transform.scale(load_image('blood.jpg', -1), (10, 10)))]
    for scale in (10, 10):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particle_group)
        self.kol = 0
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 0.5

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.kol += 8
        if self.kol >= 50:
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def terminate():
    fon2 = pygame.transform.scale(load_image('go.jpg'), (550, 550))
    screen.blit(fon2, (0, 0))
    pygame.display.flip()
    pygame.mixer.Sound.set_volume(soundb, 0)
    time.sleep(0.5)
    soundeg.play(0)
    time.sleep(1.5)
    soundgo.play(0)
    time.sleep(2)
    pygame.quit()
    sys.exit()


def good_end():
    fon3 = pygame.transform.scale(load_image('game-over.jpg'), (550, 550))
    screen.blit(fon3, (0, 0))
    pygame.display.flip()
    pygame.mixer.Sound.set_volume(soundb, 0)
    time.sleep(7)
    soundge.play(0)
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [""]
    fon = pygame.transform.scale(load_image('fon.png'), (550, 550))
    screen.blit(fon, (0, 0))
    panel('Нажмите для продолжения', 60, 500, 50)
    soundm.play(0)
    font = pygame.font.Font(None, 37)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(10, 20, 90))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.set_volume(soundm, 0)
                pygame.mixer.Channel(2)
                soundb.play(-1)
                return
        pygame.display.flip()
        clock.tick(FPS)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


start_screen()
camera = Camera()

tile_images = {'wall': pygame.transform.scale(load_image('wall.jpg', -1), (50, 50)),
               'empty': pygame.transform.scale(load_image('ff.jpg', -1), (50, 50)),
               'water': pygame.transform.scale(load_image('water.jpg'), (50, 50)),
               'stone': pygame.transform.scale(load_image('stone.jpg', -1), (50, 50)),
               'stone1': pygame.transform.scale(load_image('stone1.jpg', -1), (50, 50)),
               'stone2': pygame.transform.scale(load_image('stone2.png', -1), (50, 50)),
               'ground': pygame.transform.scale(load_image('ground.jpg'), (50, 50)),
               'flag': pygame.transform.scale(load_image('flag.jpg', -1), (50, 50)),
               'floor': pygame.transform.scale(load_image('ff.jpg', -1), (50, 50)),
               'wall2': pygame.transform.scale(load_image('wall2.jpg', -1), (50, 50)),
               'tree': pygame.transform.scale(load_image('tree.jpg', -1), (50, 50)),
               'lava': pygame.transform.scale(load_image('lava.png', -1), (50, 50)),
               'chest': pygame.transform.scale(load_image('chest.jpg', -1), (50, 50)),
               'princess': pygame.transform.scale(load_image('princess.png', -1), (50, 50)),
               'potion': pygame.transform.scale(load_image('potion.jpg', -1), (50, 50))}
player_image = pygame.transform.scale(load_image('url1.jpg', -1), (40, 50))
tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
mob_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
princess_group = pygame.sprite.Group()
chest_group = pygame.sprite.Group()

player, level_x, level_y, a = generate_level(load_level(lvl[level_number]))
for i in a:
    mob = AnimatedSprite(load_image('mob1.png', -1), 15, 1, i[0], i[1])
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_w:
                player.move(0, -1)
                if pygame.sprite.spritecollide(player, walls_group, False):
                    player.move(0, 1)
                elif pygame.sprite.spritecollide(player, mob_group, False):
                    xp = xxp(xp)
                    if xp <= 0:
                        terminate()
                elif pygame.sprite.spritecollide(player, potion_group, False):
                    xp = potion(xp)
                    for sprite in potion_group:
                        sprite.kill()
                elif pygame.sprite.spritecollide(player, lava_group, False):
                    xp = lava(xp)
                    terminate()
                elif pygame.sprite.spritecollide(player, princess_group, False):
                    level_number += 1
                    soundge.play(0)
                    for sprite in tiles_group:
                        sprite.kill()
                    for sprite in player_group:
                        sprite.kill()
                    good_end()
            if key == pygame.K_s:
                player.move(0, 1)
                if pygame.sprite.spritecollide(player, walls_group, False):
                    player.move(0, -1)
                elif pygame.sprite.spritecollide(player, mob_group, False):
                    xp = xxp(xp)
                    if xp <= 0:
                        terminate()
                elif pygame.sprite.spritecollide(player, potion_group, False):
                    xp = potion(xp)
                    for sprite in potion_group:
                        sprite.kill()
                elif pygame.sprite.spritecollide(player, lava_group, False):
                    xp = lava(xp)
                    terminate()
                elif pygame.sprite.spritecollide(player, princess_group, False):
                    level_number += 1
                    soundge.play(0)
                    for sprite in tiles_group:
                        sprite.kill()
                    for sprite in player_group:
                        sprite.kill()
                    good_end()
            if key == pygame.K_d:
                if turn != 1:
                    player.move(1, 0)
                    turn = 1
                    all_sprites.update(event)
                    if pygame.sprite.spritecollide(player, walls_group, False):
                        player.move(-1, 0)
                    elif pygame.sprite.spritecollide(player, mob_group, False):
                        xp = xxp(xp)
                        if xp <= 0:
                            terminate()
                    elif pygame.sprite.spritecollide(player, potion_group, False):
                        xp = potion(xp)
                        for sprite in potion_group:
                            sprite.kill()
                    elif pygame.sprite.spritecollide(player, lava_group, False):
                        xp = lava(xp)
                        terminate()
                    elif pygame.sprite.spritecollide(player, princess_group, False):
                        level_number += 1
                        soundge.play(0)
                        for sprite in tiles_group:
                            sprite.kill()
                        for sprite in player_group:
                            sprite.kill()
                        good_end()
                else:
                    player.move(1, 0)
                    turn = 1
                    if pygame.sprite.spritecollide(player, walls_group, False):
                        player.move(-1, 0)
                    elif pygame.sprite.spritecollide(player, mob_group, False):
                        xp = xxp(xp)
                        if xp <= 0:
                            terminate()
                    elif pygame.sprite.spritecollide(player, lava_group, False):
                        xp = lava(xp)
                        terminate()
                    elif pygame.sprite.spritecollide(player, princess_group, False):
                        level_number += 1
                        soundge.play(0)
                        for sprite in tiles_group:
                            sprite.kill()
                        for sprite in player_group:
                            sprite.kill()
                        good_end()
            if key == pygame.K_a:
                if turn != 0:
                    player.move(-1, 0)
                    turn = 0
                    all_sprites.update(event)
                    if pygame.sprite.spritecollide(player, walls_group, False):
                        player.move(1, 0)
                    elif pygame.sprite.spritecollide(player, mob_group, False):
                        xp = xxp(xp)
                        if xp <= 0:
                            terminate()
                    elif pygame.sprite.spritecollide(player, lava_group, False):
                        xp = lava(xp)
                        terminate()
                    elif pygame.sprite.spritecollide(player, princess_group, False):
                        level_number += 1
                        soundge.play(0)
                        for sprite in tiles_group:
                            sprite.kill()
                        for sprite in player_group:
                            sprite.kill()
                        good_end()
                else:
                    player.move(-1, 0)
                    turn = 0
                    if pygame.sprite.spritecollide(player, walls_group, False):
                        player.move(1, 0)
                    elif pygame.sprite.spritecollide(player, mob_group, False):
                        xp = xxp(xp)
                        if xp <= 0:
                            terminate()
                    elif pygame.sprite.spritecollide(player, potion_group, False):
                        xp = potion(xp)
                        for sprite in potion_group:
                            sprite.kill()
                    elif pygame.sprite.spritecollide(player, lava_group, False):
                        xp = lava(xp)
                        terminate()
                    elif pygame.sprite.spritecollide(player, princess_group, False):
                        level_number += 1
                        soundge.play(0)
                        for sprite in tiles_group:
                            sprite.kill()
                        for sprite in player_group:
                            sprite.kill()
                        good_end()
            elif key == pygame.K_r:
                xp = 100
                soundrl.play(0)
                for sprite in tiles_group:
                    sprite.kill()
                for sprite in player_group:
                    sprite.kill()
                player, level_x, level_y, a = generate_level(load_level(lvl[level_number]))
            elif pygame.sprite.spritecollide(player, flag_group, False):
                if not mob_group:
                    point += 100
                    panel('Очки:', 20, 75, 35)
                    panel(str(point), 75, 75, 35)
                    level_number += 1
                    if level_number == 5:
                        break
                else:
                    soundnl.play(0)
                    for sprite in mob_group:
                        sprite.kill()
                    for sprite in tiles_group:
                        sprite.kill()
            elif pygame.sprite.spritecollide(player, chest_group, False):
                soundco.play(0)
                point += 50
                panel('Очки:', 20, 75, 35)
                panel(str(point), 75, 75, 35)
                for sprite in chest_group:
                    sprite.kill()
                for sprite in player_group:
                    sprite.kill()
            player, level_x, level_y, a = generate_level(load_level(lvl[level_number]))
        if key == pygame.K_p:
            if flag:
                pygame.mixer.Sound.set_volume(soundb, 0)
                pygame.mixer.Sound.set_volume(soundis, 0)
                pygame.mixer.Sound.set_volume(soundws, 0)
                pygame.mixer.Sound.set_volume(soundeg, 0)
                pygame.mixer.Sound.set_volume(soundgo, 0)
                pygame.mixer.Sound.set_volume(soundm, 0)
                pygame.mixer.Sound.set_volume(soundrl, 0)
                pygame.mixer.Sound.set_volume(soundnl, 0)
                pygame.mixer.Sound.set_volume(sounddp, 0)
                flag = 0
            else:
                pygame.mixer.Sound.set_volume(soundb, 0.5)
                pygame.mixer.Sound.set_volume(soundis, 1)
                pygame.mixer.Sound.set_volume(soundws, 1)
                pygame.mixer.Sound.set_volume(soundeg, 1)
                pygame.mixer.Sound.set_volume(soundgo, 1)
                pygame.mixer.Sound.set_volume(soundrl, 1)
                pygame.mixer.Sound.set_volume(soundnl, 1)
                pygame.mixer.Sound.set_volume(sounddp, 1)
                flag = 1
    if event.type == pygame.MOUSEBUTTONDOWN:
        damage(pygame.mouse.get_pos())
camera.update(player)
for sprite in all_sprites:
    camera.apply(sprite)
if level_number == 2 or level_number == 3:
    fon1 = pygame.transform.scale(load_image('floor.jpg'), (550, 550))
    screen.blit(fon1, (0, 0))
    font = pygame.font.Font(None, 30)
else:
    fon1 = pygame.transform.scale(load_image('grass.png'), (550, 550))
    screen.blit(fon1, (0, 0))
    font = pygame.font.Font(None, 30)
particle_group.update()
particle_group.draw(screen)
mob_group.update()
mob_group.draw(screen)
all_sprites.draw(screen)
panel(str(xp), 40, 40, 35)
pygame.display.flip()

pygame.quit()
