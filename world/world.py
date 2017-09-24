from pygame import image
from pygame import Rect
import os
import numpy as np
import random

MAX_TILE_ID = 1
TILE_WIDTH = TILE_HEIGHT = 32


class World:
    def __init__(self, screen, screen_size, world_max_x=100, world_max_y=100):
        self.screen = screen
        self.screen_size = screen_size
        self.tile_holder = self.reset_tiles(world_max_x, world_max_y)
        self.tileset_bitmap = self.load_tileset("world/tiles_raw")
        self.tileset_rect = self.tileset_bitmap.get_rect()
        self.randomize()
        self.offset = (0,0)

    def load_tileset(self, image_path):
        return image.load(os.path.join(image_path, 'tileset.png')).convert()

    def reset_tiles(self, max_x, max_y):
        return np.zeros((max_x, max_y))

    def paint_tile(self, x, y, tile_id):
        self.tile_holder[x, y] = tile_id

    def update_world_offset(self, x, y):
        self.offset = (x, y)

    def render_tile(self, screen, x, y):
        tile_id = self.tile_holder[x, y]
        screen_pos = self.apply_offset(Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), self.offset)
        tileset_pos = Rect(tile_id * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT)

        screen.blit(self.tileset_bitmap, screen_pos, tileset_pos)


    def randomize(self):
        self.offset = (-200, -200)
        # randomize all tiles
        for y in range(self.screen_size[1]):
            for x in range(self.screen_size[0]):
                self.tile_holder[x,y] = random.randint(0,1)

        # example of 2d array slicing, ex: slicing whole column or row
        # set a couple roads: one horizontal, one vertical.
        self.tile_holder[1,:] = 2
        self.tile_holder[:,2] = 2

    @staticmethod
    def apply_offset(screen_rect, offset):
        screen_rect.left -= offset[0]
        screen_rect.top -= offset[1]
        return screen_rect

    def draw(self):
        # TODO loop only player screen
        for y in range(self.screen_size[1]):
            for x in range(self.screen_size[0]):
                self.render_tile(self.screen, x, y)
