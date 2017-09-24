from pygame import sprite, surface
from pygame.locals import color
colors = color.THECOLORS

class Player(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = surface.Surface((32,32))
        self.position = (150, 150)
        self.movepos = (0, 0)
        self.image.fill(colors['green'])
        self.rect = self.image.get_rect().move(self.position)
        self.speed = 5
        self.dx = self.dy = 0


    def update(self):
        self.dx, self.dy = self.movepos[0] * self.speed, self.movepos[1] * self.speed
        next_pos = self.rect.move(self.dx, self.dy)
        #if game_area.contains(next_pos):
        self.rect = self.rect.move(self.dx, self.dy)
        self.position = self.position[0] + self.dx, self.position[1] + self.dy
