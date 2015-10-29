from random import randint

import pygame

from Stand import Stand
from Zombie import Zombie
from Popup import *

fnt_size = 50
fnt_color = (0, 0, 0)

txt_remaining_pos = (0, 0)
txt_wave_pos = (800, 0)
txt_health_pos = (1400, 0)

class Level:
    def __init__(self, i):
        self.count = int(i * 1.5)
        self.wave = 1
        self.health_max = 100
        self.health = self.health_max

        self.paused = False
        self.game_over = False

        self.font = pygame.font.init()
        self.font = pygame.font.Font("resources/fonts/Lato-Regular.ttf", fnt_size)

        self.txt_remaining = self.font.render("Wave remaining: " + str(self.count), True, fnt_color)
        self.txt_wave = self.font.render("Wave number: " + str(self.wave), True, fnt_color)
        self.txt_health = self.font.render("Health: ", True, fnt_color)

        self.stand = Stand()
        self.enemies = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
        self.stand = pygame.sprite.GroupSingle(self.stand)
        self.stains = pygame.sprite.Group()
#TODO built table and draw it when game over


    def update(self):
        if not self.paused:
            self.update_enemies()
            self.stains.update()
            random = randint(0, 30)
            if self.count > 0 and random == 1:
                self.count -= 1
                self.txt_remaining = self.font.render("Wave remaining: " + str(self.count), True, fnt_color)
                rand = randint(0, 2)
                val = rand * 130 + 500
                zombie = Zombie(val, rand, self)
                self.enemies[rand].add(zombie)
            if self.count == 0 and self.no_enemies_left():
                self.wave += 1
                self.count = 10 * self.wave
                # TODO betere curve voor zombiespawn
                self.txt_remaining = self.font.render("Wave remaining: " + str(self.count), True, fnt_color)
                self.txt_wave = self.font.render("Wave number: " + str(self.wave), True, fnt_color)
        else:
            pass #TODO pause menu???

    def getRemaining(self):
        return int(self.count)

    def draw(self, screen):
        self.stand.draw(screen)
        self.draw_enemies(screen)
        screen.blit(self.txt_remaining, txt_remaining_pos)
        screen.blit(self.txt_wave, txt_wave_pos)
        screen.blit(self.txt_health, txt_health_pos)
        self.draw_healthbar(screen)
        self.stains.draw(screen)
        if self.game_over:
            self.popup.draw(screen)

    def shoot(self, x, y):
        if not self.paused:
            for i in [self.enemies[2], self.enemies[1], self.enemies[0]]:
                for enemy in i:
                    if enemy.hit(x, y):
                        # self.enemies[enemy.getLayer()].remove(enemy)
                        self.stains.add(BloodStain(self))
                        return
                        # self.allSprites.remove(enemy)
        else:
            self.popup.click(x, y)

    def delete_enemy(self, enemy):
        self.enemies[enemy.getLayer()].remove(enemy)

    def update_enemies(self):
        self.enemies[0].update()
        self.enemies[1].update()
        self.enemies[2].update()

    def draw_enemies(self, screen):
        self.enemies[0].draw(screen)
        self.enemies[1].draw(screen)
        self.enemies[2].draw(screen)

    def no_enemies_left(self):
        return len(self.enemies[0]) == 0 and len(self.enemies[1]) == 0 and len(self.enemies[2]) == 0

    def deletestain(self, stain):
        self.stains.remove(stain)

    def draw_end_round_stats(self):
        pass

    def draw_healthbar(self, screen):
        pygame.draw.line(screen, (0, 0, 0), [1600, 30], [1900, 30], 45)
        if self.health > 0:
            pygame.draw.line(screen, (0, 255, 0), [1600, 30], [1600 + (1900-1600)*self.health/self.health_max, 30], 45)

    def decrease_health(self, value):
        if self.health - value <= 0:
            self.health = 0
            self.paused = True
            self.game_over = True
            self.popup = Popup(PopupType.gameover, self)
        else:
            self.health -= value

    def replay(self):
        self.health = self.health_max
        self.paused = False
        self.game_over = False
        self.count = 15
        self.wave = 1
        self.enemies = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
        self.stains = pygame.sprite.Group()



class BloodStain(pygame.sprite.Sprite):

    blood = []
    for i in range(1, 9):
        blood.append(pygame.image.load("resources/images/blood/blood"+ str(i) + ".png"))

    def __init__(self, level):
        super().__init__()
        self.image = self.blood[randint(0, len(self.blood) - 1)].convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.image.set_alpha(255)
        self.rect.x = randint(0, 1920 - self.rect.width)
        self.rect.y = randint(0, 1080 - self.rect.height)
        self.level = level

    def update(self):
        alpha = self.image.get_alpha()
        if not alpha - 2 <= 0:
            self.image.set_alpha(alpha - 2)
        else:
            self.level.deletestain(self)



"""############################## Begin Popup ###################################"""


def textHollow(font, message, fontcolor):
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img


def textOutline(font, message, fontcolor, outlinecolor):
    base = font.render(message, 0, fontcolor)
    outline = textHollow(font, message, outlinecolor)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img


class Popup():

    back = pygame.image.load("resources/images/menu/popup.png")
    back_dimen = [back.get_rect().width, back.get_rect().height]
    pygame.font.init()
    font_title = pygame.font.Font("resources/fonts/LuckiestGuy.ttf", 50)

    btn_back = pygame.image.load("resources/images/menu/button.png")
    btn_dimen = [btn_back.get_rect().width, btn_back.get_rect().height]

    def __init__(self, type, level):
        self.level = level
        self.x = (1920-self.back.get_rect().width)/2
        self.y = (1080-self.back.get_rect().height)/2
        self.todraw = []
        self.buttons = []
        if PopupType.gameover == type:
            self.txt_title = textOutline(self.font_title, "Game Over", (255, 255, 255), (27, 70, 32))
            self.txt_title_pos = [self.x + (self.back.get_rect().width - self.txt_title.get_rect().width)/2, self.y + 40]
            self.buttons.append(Button(ButtonType.replay, self.font_title, self.x, self.y + self.back_dimen[1] - self.btn_dimen[1]/2, level))
            self.buttons.append(Button(ButtonType.exit, self.font_title, self.x + self.back_dimen[0] - self.btn_dimen[0], self.y + self.back_dimen[1] - self.btn_dimen[1]/2, level))


    def draw(self, screen):
        screen.blit(self.back, [self.x, self.y])
        screen.blit(self.txt_title, self.txt_title_pos)
        for i in self.buttons:
            i.draw(screen)

    def click(self, x, y):
        for i in self.buttons:
            i.click(x, y)


class Button(pygame.sprite.Sprite):

    back = pygame.image.load("resources/images/menu/button.png")

    def __init__(self, type, font, x, y, level):
        super().__init__()
        self.image = self.back
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type
        self.level = level
        if ButtonType.replay == type:
            self.txt = textOutline(font, "Replay", (255, 255, 255), (27, 70, 32))
        elif ButtonType.exit == type:
            self.txt = textOutline(font, "Exit", (255, 255, 255), (27, 70, 32))
        self.txt_pos = [self.rect.x + (self.back.get_rect().width - self.txt.get_rect().width)/2, self.rect.y +(self.back.get_rect().height - self.txt.get_rect().height)/2]

    def draw(self, screen):
        screen.blit(self.back, self.rect)
        screen.blit(self.txt, self.txt_pos)

    def click(self, x, y):
        if self.rect.collidepoint(x, y):
            if ButtonType.replay == self.type:
                self.level.replay()
            if ButtonType.exit == self.type:
                pygame.quit()

class TextGrid():

    desc_width = 200
    elem_width = 100
    cell_height = 30
    fnt_color = (0, 0, 0)

    def __init__(self, font, x, y):
        self.font = font
        self.array = []
        self.addRow("desc", "Your score", "Highscore")
        self.x = x
        self.y = y

    def addRow(self, desc, ownScore, highScore):
        self.array.append([self.getFont(desc), self.getFont(ownScore), self.getFont(highScore)])

    def getFont(self, text):
        return self.font.render(text, True, fnt_color)

    def draw(self, screen):
        for i in range(0, len(self.array) - 1):
            for x in range(0, len(self.array[i]) - 1):
                screen.blit(self.array[i][x], [self.x + 0 if x==0 else self.x + self.desc_width + (x-1)*self.elem_width,self.y + self.cell_height*i])


class PopupType(Enum):
    gameover = 0


class ButtonType(Enum):
    replay = 0
    exit = 1