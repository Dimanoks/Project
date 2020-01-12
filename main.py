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
size = width, height = 550, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
xp = 100
k = 0
f = 1
lvl = ['map1.txt', 'map2.txt', 'map3.txt']


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
                # AnimatedSprite(pygame.transform.scale(load_image('url.jpg', -1), (200, 50)), 4, 1, x-25, y-25)
                sound = mixer.Sound('data/impact by sword.ogg')
                sound.play(0)
                sprite.kill()
                create_particles(pygame.mouse.get_pos())
            else:
                sound = mixer.Sound('data/a wave of the sword.ogg')
                sound.play(0)


def lava(xp):
    xp = 0
    return int(xp)


def potion(xp):
    sound = mixer.Sound('data/drinking a potion.ogg')
    sound.play(0)
    if xp > 50:
        xp += (100 - xp)
        print(xp)
    else:
        xp += 50
        print(xp)
    return int(xp)


def xxp(xp):
    n = (random.randrange(3) - 1)
    if n == 1:
        xp -= 75
        print(xp)
        return int(xp)
    elif n == 0:
        xp -= 50
        print(xp)
        return int(xp)
    else:
        xp -= 25
        print(xp)
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



class Panel:
    def __init__(self):
        font = pygame.font.Font(None, 24)



def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
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
            elif level[y][x] == 'g':
                Tile('ground', x, y)
            elif level[y][x] == '1':
                Tile('mob', x, y)
            elif level[y][x] == '!':
                Tile('flag', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                px, py = x, y
                new_player = Player(px, py)
    return new_player, x, y


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group_hit)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
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
        if f == 0:
            self.image = pygame.transform.flip(self.image, True, False)
        elif f == 1:
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
    sound = mixer.Sound('data/end game.ogg')
    sound.play(0)
    time.sleep(1.5)
    sound1 = mixer.Sound('data/game over.ogg')
    sound1.play(0)
    time.sleep(2)
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["     Adventure of the knight"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (550, 550))
    screen.blit(fon, (0, 0))
    soundS = mixer.Sound('data/monster.ogg')
    soundS.play(0)
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
                pygame.mixer.Sound.set_volume(soundS, 0)
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


camera = Camera()
start_screen()

tile_images = {'wall': pygame.transform.scale(load_image('wall.jpg', -1), (50, 50)),
               'empty': pygame.transform.scale(load_image('ff.jpg', -1), (50, 50)),
               'mob': pygame.transform.scale(load_image('mob1_1.png', -1), (50, 50)),
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
player_group_hit = pygame.sprite.Group()

player, level_x, level_y = generate_level(load_level(lvl[k]))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_UP:
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
            if key == pygame.K_DOWN:
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
            if key == pygame.K_RIGHT:
                if f != 1:
                    player.move(1, 0)
                    f = 1
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
                else:
                    player.move(1, 0)
                    f = 1
                    if pygame.sprite.spritecollide(player, walls_group, False):
                        player.move(-1, 0)
                    elif pygame.sprite.spritecollide(player, mob_group, False):
                        xp = xxp(xp)
                        if xp <= 0:
                            terminate()
                    elif pygame.sprite.spritecollide(player, lava_group, False):
                        xp = lava(xp)
                        terminate()
            if key == pygame.K_LEFT:
                if f != 0:
                    player.move(-1, 0)
                    f = 0
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
                else:
                    player.move(-1, 0)
                    f = 0
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
            elif pygame.sprite.spritecollide(player, flag_group, False):
                k += 1
                sound = mixer.Sound('data/The sound of going to the next level.ogg')
                sound.play(0)
                for sprite in tiles_group:
                    sprite.kill()
                for sprite in player_group:
                    sprite.kill()
                player, level_x, level_y = generate_level(load_level(lvl[k]))
        if event.type == pygame.MOUSEBUTTONDOWN:
            damage(pygame.mouse.get_pos())

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    if k == 2:
        fon1 = pygame.transform.scale(load_image('floor.jpg'), (550, 550))
        screen.blit(fon1, (0, 0))
        font = pygame.font.Font(None, 30)
    else:
        fon1 = pygame.transform.scale(load_image('grass.png'), (550, 550))
        screen.blit(fon1, (0, 0))
        font = pygame.font.Font(None, 30)
    particle_group.update()
    particle_group.draw(screen)
    player_group_hit.update()
    player_group_hit.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
