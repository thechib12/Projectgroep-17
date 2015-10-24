import pygame

__author__ = 'reneb_000'


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        # init pygame sprite class
        super().__init__()
        # set the image of the object
        self.image = pygame.image.load("images/crosshairs/crosshair1.png").convert_alpha()
        # self.image.fill([0, 0, 0])
        self.rect = self.image.get_rect()

    def setXY(self, x, y):
        self.rect.x = x - self.rect.width/2
        self.rect.y = y - self.rect.height/2

    def update(self):
        pos = pygame.mouse.get_pos()
        self.setXY(pos[0], pos[1])

