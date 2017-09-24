from pygame import sprite, surface
from pygame.locals import color
import random
colors = color.THECOLORS


def random_pos_neg():
    return 1 if random.randint(0,100) >= 50 else -1

class Enemy(sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = surface.Surface((20,20))
        self.image.fill(colors['red'])
        self.rect = self.image.get_rect().move(random.randint(0, 600), random.randint(0, 600))
        self.speed = random.randint(1, 5)
        self.movepos = [random_pos_neg(), random_pos_neg()]


    def update(self):
        dx, dy = self.movepos[0] * self.speed, self.movepos[1] * self.speed
        self.rect = self.rect.move(dx, dy)
        #if not game_area.contains(self.rect):
        #print("An enemy died")
        #self.kill()

        '''
        if self.rect[0] < game_area[0] or self.rect[0] + self.rect[2] > game_area[2]:
            self.rect.move(-dx, -dy)
            self.movepos[0] = -self.movepos[0]
        if self.rect[1] < game_area[1] or self.rect[1] + self.rect[3] > game_area[3]:
            self.rect.move(-dx, -dy)
            self.movepos[1] = -self.movepos[1]
        '''