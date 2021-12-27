import pygame
import os


# загрузка фото
def load_image(s, key=None):
    name = os.path.join("data", s)
    try:
        image = pygame.image.load(name).convert()
    except pygame.error as message:
        print("error with " + s)
        raise SystemExit(message)
    if key is not None:
        if key == -1:
            key = image.get_at((0, 0))
            image.set_colorkey(key)
        elif key == -2:
            key = image.get_at((0, 0))
            image.set_colorkey(key)
            key = image.get_at((949, 0))
            image.set_colorkey(key)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("@godofnatural")
screen.fill("black")
clock = pygame.time.Clock()
fps = 60
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
heroes = pygame.sprite.Group()
boxes = pygame.sprite.Group()
water_jumping_start = pygame.USEREVENT + 1
fire_jumping_start = pygame.USEREVENT + 2


# персонажы
class Heroes(pygame.sprite.Sprite):
    def __init__(self, x, y, hero):
        super().__init__(all_sprites)
        self.add(heroes)
        self.hero = hero
        if self.hero == "fire":
            self.image = load_image("fire-bg.png", -1)
        else:
            self.image = load_image("water-bg.png", -1)
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.jump_flag = False

    # гравитация
    def update(self):
        if not pygame.sprite.spritecollideany(self, platforms)\
                and not pygame.sprite.spritecollideany(self, boxes):
            self.rect = self.rect.move(0, 200 / fps)

    # движение вправо
    def right(self):
        self.rect = self.rect.move(4, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect = self.rect.move(200 / fps, 0)
        self.rect = self.rect.move(-4, 5)

    # движение влево
    def left(self):
        self.rect = self.rect.move(-4, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect = self.rect.move(-(200 / fps), 0)
        self.rect = self.rect.move(4, 5)

    def jump(self):
        self.rect = self.rect.move(0, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect = self.rect.move(0, -400 / fps)
        else:
            self.jump_flag = False
        self.rect = self.rect.move(0, 5)


# платформа(составляет стены, пол уровня, остальные препятствия)
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(platforms)
        self.image = load_image("stone.png")
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)


# плотный блок
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(boxes)
        self.image = load_image("box.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect = self.rect.move(0, 200 / fps)

    def right(self):
        self.rect = self.rect.move(1, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            if pygame.sprite.spritecollideany(self, heroes):
                self.rect = self.rect.move(200 / fps, 0)
        self.rect = self.rect.move(-1, 5)

    def left(self):
        self.rect = self.rect.move(-1, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            if pygame.sprite.spritecollideany(self, heroes):
                self.rect = self.rect.move(-(200 / fps), 0)
        self.rect = self.rect.move(1, 5)


# загрузка уровня
def load_level():
    name = os.path.join("levels", "test.txt")
    with open(name) as f:
        raws = f.readlines()
        for i in range(len(raws)):
            for j in range(len(raws[i])):
                if raws[i][j] == "1":
                    Platform(20 + j * 24, 28 + i * 24)


load_level()
pl2 = Heroes(110, 670, "water")
pl1 = Heroes(50, 670, "fire")
box1 = Box(200, 580)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pygame.time.set_timer(water_jumping_start, 650)
                pl2.jump_flag = True
            if event.key == pygame.K_w:
                pygame.time.set_timer(fire_jumping_start, 650)
                pl1.jump_flag = True
        if event.type == fire_jumping_start:
            if not pl1.jump_flag:
                pygame.time.set_timer(fire_jumping_start, 0)
            else:
                pl1.jump_flag = False
        if event.type == water_jumping_start:
            if not pl2.jump_flag:
                pygame.time.set_timer(water_jumping_start, 0)
            else:
                pl2.jump_flag = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        pl1.right()
        box1.right()
    if keys[pygame.K_a]:
        pl1.left()
        box1.left()
    if keys[pygame.K_RIGHT]:
        pl2.right()
        box1.right()
    if keys[pygame.K_LEFT]:
        pl2.left()
        box1.left()
    if pl1.jump_flag:
        pl1.jump()
    if pl2.jump_flag:
        pl2.jump()

    all_sprites.update()
    screen.fill("black")
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
