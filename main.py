import pygame, os, sys, random

pygame.init()
n = 100
def xxp(n):
    xp = (random.randrange(3) - 1)
    if xp == 1:
        n -= 100
        print(n)
        return int(n)
    elif xp == 0:
        n -= 50
        print(n)
        return int(n)
    else:
        n -= 25
        print(n)
        return int(n)

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
            elif level[y][x] == '/':
                Tile('water', x, y)
            elif level[y][x] == '0':
                Tile('stone', x, y)
            elif level[y][x] == '2':
                Tile('stone1', x, y)
            elif level[y][x] == '3':
                Tile('stone2', x, y)
            elif level[y][x] == 'g':
                Tile('ground', x, y)
            elif level[y][x] == '1':
                Tile('mob', x, y)
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
                tile_type == 'water':
            self.add(walls_group)
        elif tile_type == 'mob':
            self.add(mob_group)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5, tile_height * pos_y)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(tile_width * x + self.rect.x, tile_height * y + self.rect.y)
FPS = 50

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["                Adventure of the knight"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (550, 550))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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
                return  # начинаем игру
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

size = width, height = 550, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_screen()


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass1.png'),
               'mob': pygame.transform.scale(load_image('mob1_1.png'), (50, 50)),
               'water': pygame.transform.scale(load_image('water.jpg'), (50, 50)),
               'stone': pygame.transform.scale(load_image('stone.jpg', -1), (50, 50)),
               'stone1': pygame.transform.scale(load_image('stone1.jpg', -1), (50, 50)),
               'stone2': pygame.transform.scale(load_image('stone2.png', -1), (50, 50)),
               'ground': pygame.transform.scale(load_image('ground.jpg'), (50, 50))}
player_image = pygame.transform.scale(load_image('url1.jpg'), (40, 50))
tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
mob_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()

player, level_x, level_y = generate_level(load_level('map2.txt'))
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
                if pygame.sprite.spritecollide(player, mob_group, False):
                    n = xxp(n)
                    if n <= 0:
                        terminate()
            if key == pygame.K_DOWN:
                player.move(0, 1)
                if pygame.sprite.spritecollide(player, walls_group, False):
                    player.move(0, -1)
                if pygame.sprite.spritecollide(player, mob_group, False):
                    n = xxp(n)
                    if n <= 0:
                        terminate()
            if key == pygame.K_RIGHT:
                player.move(1, 0)
                if pygame.sprite.spritecollide(player, walls_group ,False):
                    player.move(-1, 0)
                if pygame.sprite.spritecollide(player, mob_group, False):
                    n = xxp(n)
                    if n <= 0:
                        terminate()
            if key == pygame.K_LEFT:
                player.move(-1, 0)
                if pygame.sprite.spritecollide(player, walls_group, False):
                    player.move(1, 0)
                if pygame.sprite.spritecollide(player, mob_group, False):
                    n = xxp(n)
                    if n <= 0:
                        terminate()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill(pygame.Color("white"))
    all_sprites.draw(screen)

    pygame.display.flip()


pygame.quit()