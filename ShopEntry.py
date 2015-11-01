import pygame
from Level import textOutline, Button, ButtonType

__author__ = 'reneb_000'


class Shop():

    def __init__(self, cursor, stateobj):
        self.cursor = cursor

        btn_back = pygame.image.load("resources/images/menu/button.png")
        btn_dimen = [btn_back.get_rect().width, btn_back.get_rect().height]

        self.back = pygame.image.load("resources/images/menu/popup.png").convert_alpha()
        self.back_pos = (1920-self.back.get_rect().width)/2, (1080-self.back.get_rect().height)/2
        self.back_dimen = [self.back.get_rect().width, self.back.get_rect().height]
        font_title = pygame.font.Font("resources/fonts/LuckiestGuy.ttf", 50)
        self.txt_title = textOutline(font_title, "Shop", (255, 255, 255), (27, 70, 32))
        self.txt_title_pos = [self.back_pos[0] + (self.back.get_rect().width - self.txt_title.get_rect().width)/2, self.back_pos[1] + 40]
        self.button = Button(ButtonType.back, font_title, self.back_pos[0] + (self.back_dimen[0] - btn_dimen[0])/2, self.back_pos[1] + self.back_dimen[1] - btn_dimen[1]/2, None, stateobj)

        self.items = []
        for i in range(0, 8):
            self.items.append(ShopEntry(i, self.back_pos[0]+150, self.back_pos[1]+150, cursor))

    def draw(self, screen):
        screen.blit(self.back, self.back_pos)
        screen.blit(self.txt_title, self.txt_title_pos)
        for item in self.items:
            item.draw(screen)
        self.button.draw(screen)

    def click(self, x, y):
        self.button.click(x, y)
        for item in self.items:
            item.click(x, y)

class ShopEntry():

    sprite = []
    for i in range(0, 8):
        sprite.append(pygame.image.load("resources/images/crosshairs/crosshair"+str(i)+".png").convert_alpha())
    btn_back = pygame.image.load("resources/images/menu/button.png").convert_alpha()
    button = pygame.transform.scale(btn_back, (int(btn_back.get_rect().width/2), int(btn_back.get_rect().width/2)))

    def __init__(self, sprite_index, startx, starty, cursor):
        self.cursor = cursor
        self.x = startx + sprite_index%3 * self.sprite[0].get_rect().width
        self.y = starty + sprite_index//3 * self.sprite[0].get_rect().height
        self.sprite = self.sprite[sprite_index]
        self.rect = self.sprite.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def click(self, x, y):
        if self.rect.collidepoint(x, y):
            self.cursor.set_image(self.sprite)

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
