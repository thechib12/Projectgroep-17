import pygame

__author__ = 'reneb_000'


class Zombie(pygame.sprite.Sprite):
    def __init__(self, own_height, y):
        # init pygame sprite class
        super().__init__()
        self.sheet = pygame.image.load("images/enemies/zombie3.png")
        self.index = 0
        self.real_height = own_height
        self.real_width =  self.sheet.get_rect().width
        self.max_index = self.sheet.get_rect().height/self.real_height
        self.sheet.set_clip(pygame.Rect(0, self.index*self.real_height, self.real_width, self.real_height))

        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.rect = self.image.get_rect()
        self.rect.y = y

    def update(self):
        self.index = (self.index+1)%self.max_index
        self.sheet.set_clip(pygame.Rect(0, self.index*self.real_height, self.real_width, self.real_height))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect.x += 3
