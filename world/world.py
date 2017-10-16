from pygame import image
from pygame import Rect
import os
import numpy as np
import logging
import math
import json

TILEMAP_PATH = os.path.join("world/tiles_raw", 'tileset.png')
JSON_MAP_PATH = "world/maps/map.json"

logger = logging.getLogger("Game")

MAX_TILE_ID = 1
TILE_WIDTH = TILE_HEIGHT = 32

def scale_to_tiles(pixel_size):
    return int(math.ceil(pixel_size / TILE_WIDTH)) + 1

class World:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_tiles = scale_to_tiles(screen_size[0]), scale_to_tiles(screen_size[1])
        self.tile_holder = self.load_map_data()
        self.tileset_bitmap = self.load_tileset(TILEMAP_PATH)
        self.tileset_rect = self.tileset_bitmap.get_rect()
        self.offset = (0,0)
        self.prev_offset = self.offset

    def load_tileset(self, image_path):
        return image.load(image_path).convert()

    def reset_tiles(self, max_x, max_y):
        return np.zeros((max_x, max_y))

    def paint_tile(self, x, y, tile_id):
        self.tile_holder[x, y] = tile_id

    def update_world_offset(self, x, y):
        self.offset = (self.offset[0] + x, self.offset[1] + y)

    def render_tile(self, screen, x, y):
        tile_id = self.tile_holder[x, y] - 1 # Temporary fix. Tiled outputs tiles with 1-index. we use 0-index like sane people.
        screen_pos = self.apply_offset(Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), self.offset)
        tileset_pos = Rect(tile_id * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT)
        screen.blit(self.tileset_bitmap, screen_pos, tileset_pos)

    def world_size_in_pixels(self):
        return self.total_world_width, self.total_world_height

    @staticmethod
    def load_map_data():
        with open(JSON_MAP_PATH) as f:
            content = json.load(f)
        layer = content["layers"][0]
        width = layer["width"]
        height = layer["height"]

        data = layer["data"]

        return np.asarray(data).reshape(width, height)

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
        self.camera_func = self.complex_camera
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

        #TODO find somewhere better to scale to pixel-values for camera? Shouldn't need to be computed each time.
        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-((camera.width * TILE_WIDTH)-self.WIN_WIDTH), l)   # stop scrolling at the right edge
        t = max(-((camera.height * TILE_HEIGHT)-self.WIN_HEIGHT), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top

        return Rect(l, t, w, h)
