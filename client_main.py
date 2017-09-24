import pygame
import random
from pygame.locals import *
from world import world
pygame.init()
colors = pygame.color.THECOLORS
screen = pygame.display.set_mode([1024, 1024])
game_area = screen.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((32,32))
        self.position = (500, 300)
        self.movepos = (0, 0)
        self.image.fill(colors['green'])
        self.rect = self.image.get_rect().move(self.position)
        self.speed = 5

    def update(self):
        dx, dy = self.movepos[0] * self.speed, self.movepos[1] * self.speed
        next_pos = self.rect.move(dx, dy)
        if game_area.contains(next_pos):
            self.rect = self.rect.move(dx, dy)
            self.position = self.position[0] + dx, self.position[1] + dy




def random_pos_neg():
    return int(max(1, min(-1, random.uniform(-100, 100))))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.surface.Surface((20,20))
        self.image.fill(colors['red'])
        self.rect = self.image.get_rect().move(random.randint(0, 600), random.randint(0, 600))
        self.speed = random.randint(1, 5)
        self.movepos = [random_pos_neg(), random_pos_neg()]

    def update(self):
        dx, dy = self.movepos[0] * self.speed, self.movepos[1] * self.speed
        self.rect = self.rect.move(dx, dy)
        if not game_area.contains(self.rect):
            print("An enemy died")
            self.kill()


done=False
clock = pygame.time.Clock()
player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemy = Enemy()
all_sprites.add(enemy)
enemies.add(enemy)
proximity_limit = (250, 250)
game_world = world.World(screen, [100, 100], world_max_x=100, world_max_y=100)

def find_relevant_entities(main_entity, all_entities):
    close_entities = []
    for e in all_entities:
        if e.rect.inflate(proximity_limit).contains(main_entity.rect) and e is not main_entity:
            close_entities.append(e)
    return close_entities



while not done:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
        elif event.type == QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    l, r, u, d = [pressed[k] for k in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]]
    player.movepos = -l + r, -u + d
    for entity in all_sprites:
        entity.update()

    game_world.update_world_offset(player.position[0], player.position[1])
    game_world.draw()
    #screen.fill(colors['white'])
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect.topleft)

    for e in find_relevant_entities(player, all_sprites):
        print(type(e), "is close to player")

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

    pygame.display.flip()

    clock.tick(60)
