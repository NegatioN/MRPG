from pygame import image
from pygame import Rect
import os
import numpy as np
import random
import logging
import math

logger = logging.getLogger("Game")

MAX_TILE_ID = 1
TILE_WIDTH = TILE_HEIGHT = 32

def scale_to_tiles(pixel_size):
    return int(math.ceil(pixel_size / TILE_WIDTH)) + 1

class World:
    def __init__(self, screen, screen_size, world_max_x=100, world_max_y=100):
        self.screen = screen
        self.screen_tiles = scale_to_tiles(screen_size[0]), scale_to_tiles(screen_size[1])
        self.total_world_width = TILE_WIDTH * world_max_x
        self.total_world_height = TILE_HEIGHT * world_max_y
        self.tile_holder = self.reset_tiles(world_max_x, world_max_y)
        self.tileset_bitmap = self.load_tileset("world/tiles_raw")
        self.tileset_rect = self.tileset_bitmap.get_rect()
        self.randomize()
        self.offset = (0,0)
        self.prev_offset = self.offset

    def load_tileset(self, image_path):
        return image.load(os.path.join(image_path, 'tileset.png')).convert()

    def reset_tiles(self, max_x, max_y):
        return np.zeros((max_x, max_y))

    def paint_tile(self, x, y, tile_id):
        self.tile_holder[x, y] = tile_id

    def update_world_offset(self, x, y):
        self.offset = (self.offset[0] + x, self.offset[1] + y)

    def render_tile(self, screen, x, y):
        tile_id = self.tile_holder[x, y]
        screen_pos = self.apply_offset(Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), self.offset)
        tileset_pos = Rect(tile_id * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT)
        screen.blit(self.tileset_bitmap, screen_pos, tileset_pos)

    def world_size_in_pixels(self):
        return (self.total_world_width, self.total_world_height)


    def randomize(self):
        # randomize all tiles
        for y in range(self.tile_holder.shape[1]):
            for x in range(self.tile_holder.shape[0]):
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
        x_tile_num = int(self.offset[0] / TILE_WIDTH)
        y_tile_num = int(self.offset[1] / TILE_HEIGHT)
        for y in range(self.screen_tiles[1]):
            #y = int(y/TILE_HEIGHT)
            y += y_tile_num

            for x in range(self.screen_tiles[0]):
                #x = int(x/TILE_HEIGHT)
                x += x_tile_num
                self.render_tile(self.screen, x, y)
        if self.offset != self.prev_offset:
            logger.debug("world offset={}".format(self.offset))
            logger.debug("X_tile={}".format(x_tile_num))
            logger.debug("Y_tile={}".format(y_tile_num))
            self.prev_offset = self.offset


class Camera:
    def __init__(self, width, height):
        self.camera_func = self.simple_camera
        self.state = Rect(0, 0, width, height)
        self.HALF_WIDTH = int(width / 2)
        self.HALF_HEIGHT = int(height / 2)
        self.WIN_HEIGHT = height
        self.WIN_WIDTH = width


    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def simple_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        print(l, t)
        return Rect(-l+self.HALF_WIDTH, -t+self.HALF_HEIGHT, w, h)


    def complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l+self.HALF_WIDTH, -t+self.HALF_HEIGHT, w, h # center player

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width-self.WIN_WIDTH), l)   # stop scrolling at the right edge
        t = max(-(camera.height-self.WIN_HEIGHT), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top

        return Rect(l, t, w, h)
