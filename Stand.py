import pygame

__author__ = 'reneb_000'


class Stand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("resources/images/stand.png").convert_alpha()
        self.rect = self.image.get_rect();
        self.rect.x = 1920 - self.rect.width
        self.rect.y = 1080 / 2