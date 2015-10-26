from enum import Enum
import pygame
from random import randint

__author__ = 'reneb_000'
"""
two legg:
169x198
one legg:
151x201
no legg:
139x146
"""


class Zombie(pygame.sprite.Sprite):

    zombie_sheet_normal = pygame.image.load("resources/images/enemies/zombie3.png")
    zombie_sheet_one_leg = pygame.image.load("resources/images/enemies/one_leg.png")
    zombie_sheet_no_leg = pygame.image.load("resources/images/enemies/no_leg.png")

    def __init__(self, y):
        # init pygame sprite class
        super().__init__()

        # init zombie data
        self.state = State.twoLeg
        self.speed = 2


        # load the sheets
        """
        self.sheet_normal = pygame.image.load("images/enemies/zombie3.png")
        self.sheet_one_leg = pygame.image.load("images/enemies/one_leg.png")
        self.sheet_no_leg = pygame.image.load("images/enemies/no_leg.png")
        self.sheet = self.sheet_normal
        """
        self.sheet_normal = self.zombie_sheet_normal
        self.sheet_one_leg = self.zombie_sheet_one_leg
        self.sheet_no_leg = self.zombie_sheet_no_leg
        self.sheet = self.sheet_normal

        # calculate the real height en width of sprite (the size on screen)
        self.real_height = 198
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
        self.rect.x = - self.rect.width
        self.rect.y = y

    def update(self):
        self.index = (self.index + 1) % self.max_index
        self.sheet.set_clip(pygame.Rect(0, self.index * self.real_height, self.real_width, self.real_height))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect.x += self.speed

    def hit(self, x, y):
        if self.rect.collidepoint(x, y):
            if (y - self.rect.y) > self.real_height * .6:
                self.set_image_leg_less()
                return False
            return True
        return False

    def set_image_leg_less(self):
        if self.state == State.twoLeg:
            self.sheet = self.sheet_one_leg
            self.real_height = 201
            self.state = State.oneLeg
            self.calcNewCord([169, 198], [151, 201])
        elif self.state == State.oneLeg:
            self.sheet = self.sheet_no_leg
            self.real_height = 146
            self.speed = 1
            self.calcNewCord([151, 201], [139, 146])

# fix for the origin problem in pygame, if you change the sprites without calling this function, the sprite "jumps" on screen
    def calcNewCord(self, old, new):
        self.rect.x += (old[0] - new[0]) / 2
        self.rect.y += (old[1] - new[1])


class State(Enum):
    twoLeg = 0
    oneLeg = 1
    noLeg = 2
