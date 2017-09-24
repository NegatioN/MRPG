import pygame
from pygame.locals import *
from world import world
from client import player, enemy
import logging

logger = logging.getLogger("Game")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
debug = True
logger.setLevel(logging.DEBUG if debug else logging.INFO)
pygame.init()
colors = pygame.color.THECOLORS
screen_size = (1024, 1024)

screen = pygame.display.set_mode(screen_size)
MAX_FRAMERATE = 60

done=False
clock = pygame.time.Clock()
player = player.Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemy = enemy.Enemy()
all_sprites.add(enemy)
enemies.add(enemy)
proximity_limit = (250, 250)
game_world = world.World(screen, screen_size, world_max_x=1000, world_max_y=1000)
game_world.update_world_offset(player.position[0], player.position[1])

cam = world.Camera(*screen_size)

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
    game_world.draw()
    cam.update(player)

    for entity in all_sprites:
        entity.update()

    game_world.update_world_offset(player.dx, player.dy)

    for entity in all_sprites:
        screen.blit(entity.image, cam.apply(entity))

    for e in find_relevant_entities(player, all_sprites):
        print(type(e), "is close to player")

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

    pygame.display.flip()

    clock.tick(MAX_FRAMERATE)
