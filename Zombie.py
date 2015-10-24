import pygame
from random import randint

__author__ = 'reneb_000'


class Zombie(pygame.sprite.Sprite):
    def __init__(self, own_height, y):
        # init pygame sprite class
        super().__init__()

        # load the sheets
        self.sheet_normal = pygame.image.load("images/enemies/zombie3.png")
        self.sheet_one_legg = pygame.image.load("images/enemies/one_legg.png")
        self.sheet = pygame.image.load("images/enemies/zombie3.png")

        # calculate the real height en width of sprite (the size on screen)
        self.real_height = own_height
        self.real_width = self.sheet.get_rect().width

        # frame index calculation
        self.max_index = self.sheet.get_rect().height / self.real_height
        self.index = randint(0, self.max_index - 1)

        # set the frame
        self.sheet.set_clip(pygame.Rect(0, self.index * self.real_height, self.real_width, self.real_height))

        # set frame as image
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        # rectangle creation and setting of coordinates
        self.rect = self.image.get_rect()
        self.rect.y = y

    def update(self):
        self.index = (self.index + 1) % self.max_index
        self.sheet.set_clip(pygame.Rect(0, self.index * self.real_height, self.real_width, self.real_height))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect.x += 3

    def hit(self, x, y):
        if self.rect.collidepoint(x, y):
            if (y - self.rect.y) > self.real_height * .6:
                self.set_image_legg_less()
                return False
            return True
        return False

    def set_image_legg_less(self):
        self.sheet = self.sheet_one_legg
        self.real_height = 221
        # TODO animations allemaal even hoog en dezelfde verkleiningsfactor
