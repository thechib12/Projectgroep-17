from enum import Enum
import pygame
from random import randint
from pygame.constants import *
from SharedPreference import Settings

__author__ = 'reneb_000'
"""
1e = loop animatie
2e = attack animatie
3e = dead
two legg:
169x198
122x189
230x218
one legg:
151x201
122x186
230x206
no legg:
139x146
122x153
173x176
"""


class Zombie(pygame.sprite.Sprite):

    pygame.init()
    pygame.display.set_mode((1,1), pygame.NOFRAME)

    zombie_sheet_two_leg = pygame.image.load("resources/images/enemies/normal.png").convert_alpha()
    zombie_sheet_one_leg = pygame.image.load("resources/images/enemies/one_leg.png").convert_alpha()
    zombie_sheet_no_leg = pygame.image.load("resources/images/enemies/no_leg.png").convert_alpha()

    zombie_sheet_attack_two_leg = pygame.image.load("resources/images/enemies/attack_normal.png").convert_alpha()
    zombie_sheet_attack_one_leg = pygame.image.load("resources/images/enemies/attack_one_leg.png").convert_alpha()
    zombie_sheet_attack_no_leg = pygame.image.load("resources/images/enemies/attack_no_leg.png").convert_alpha()

    zombie_sheet_dead_two_leg = pygame.image.load("resources/images/enemies/dead_normal.png").convert()
    zombie_sheet_dead_two_leg.set_colorkey((255, 255, 255))
    zombie_sheet_dead_one_leg = pygame.image.load("resources/images/enemies/dead_one_leg.png").convert()
    zombie_sheet_dead_one_leg.set_colorkey((255, 255, 255))
    zombie_sheet_dead_no_leg = pygame.image.load("resources/images/enemies/dead_no_leg.png").convert()
    zombie_sheet_dead_no_leg.set_colorkey((255, 255, 255))

    sound = []
    for i in range(1, 5):
        sound.append(pygame.mixer.Sound("resources/sounds/enemy/sound" + str(i) + ".ogg"))
        sound[i-1].set_volume(0.5)

    def __init__(self, y, layer, levelobj, speed):
        # init pygame sprite class
        super().__init__()
        self.level = levelobj

        # init zombie data
        self.attacks_per_sec = 1
        self.soundscount = 0
        self.max_soundcount = 80
        self.frame_counter = 0
        self.state = State.twoLeg
        self.speed = speed
        self.layer = layer
        self.attacking = False
        self.dead = False

        # TODO test local vs static
        self.sheet_two_leg = self.zombie_sheet_two_leg
        self.sheet_one_leg = self.zombie_sheet_one_leg
        self.sheet_no_leg = self.zombie_sheet_no_leg
        self.sheet = self.sheet_two_leg

        self.sound_threshold = randint(0, self.max_soundcount)

        # calculate the real height en width of sprite (the size on screen)
        self.real_height = 198
        self.real_width = self.sheet.get_rect().width

        # frame index calculation
        self.max_index = self.sheet.get_rect().height / self.real_height
        self.index = randint(0, self.max_index - 1)
        self.alpha_count = 255
        # set the frame
        self.sheet.set_clip(pygame.Rect(0, self.index * self.real_height, self.real_width, self.real_height))

        # set frame as image
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        # rectangle creation and setting of coordinates
        self.rect = self.image.get_rect()
        self.rect.x = - self.rect.width
        self.rect.y = y

    def update(self):
        if not self.dead:
            self.frame_counter = (self.frame_counter + 1) % (30/self.attacks_per_sec)
            self.index = (self.index + 1) % self.max_index
            self.sheet.set_clip(pygame.Rect(0, self.index * self.real_height, self.real_width, self.real_height))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.rect.x += self.speed
            self.soundscount = (self.soundscount + 1) % self.max_soundcount
            if self.soundscount == self.sound_threshold:
                self.sound[randint(0, len(self.sound) - 1)].play()
        else:
            if self.index + 1 == self.max_index:
                # alpha = self.image.get_alpha()
                if self.alpha_count - 2 >= 0:
                    self.alpha_count -= 2
                    if Settings.fading:
                        self.image.set_alpha(self.alpha_count)
                else:
                    self.level.delete_enemy(self)
            else:
                self.index += 1
                self.sheet.set_clip(pygame.Rect(0, self.index * self.real_height, self.real_width, self.real_height))
                self.image = self.sheet.subsurface(self.sheet.get_clip())

        if self.rect.x >= 1250 - (2 - self.layer * self.real_width) and not self.attacking:
            self.set_attacking()

        if self.attacking and self.frame_counter == 0:
            self.level.decrease_health(1)

    def hit(self, x, y):
        if self.rect.collidepoint(x, y) and not self.dead:
            if not self.state == State.noLeg and (y - self.rect.y) > self.real_height * .6:
                self.set_image_leg_less()
                return HitType.legshot
            elif (y - self.rect.y) < self.real_height / 3 :
                self.set_dead()
                return HitType.headshot
            else:
                self.set_dead()
            return HitType.chest
        return HitType.miss

    def set_image_leg_less(self):
        if not self.attacking:
            if State.twoLeg == self.state:
                self.set_new_sprite_values(State.oneLeg, self.real_width, self.real_height, 151, 201, self.zombie_sheet_one_leg, -1)
            elif State.oneLeg == self.state:
                self.set_new_sprite_values(State.noLeg, self.real_width, self.real_height, 139, 146, self.zombie_sheet_no_leg, 1)
        else:
            if State.twoLeg == self.state:
                self.set_new_sprite_values(State.oneLeg, self.real_width, self.real_height, 122, 186, self.zombie_sheet_attack_one_leg, 0)
            elif State.oneLeg == self.state:
                self.set_new_sprite_values(State.noLeg, self.real_width, self.real_height, 122, 153, self.zombie_sheet_attack_no_leg, 0)

    def set_attacking(self):
        # TODO jumping of sprite fix
        self.attacking = True
        if State.twoLeg == self.state:
            self.set_new_sprite_values(State.twoLeg, self.real_width, self.real_height, 122, 189, self.zombie_sheet_attack_two_leg, 0)
        elif State.oneLeg == self.state:
            self.set_new_sprite_values(State.oneLeg, self.real_width, self.real_height, 122, 186, self.zombie_sheet_attack_one_leg, 0)
        elif State.noLeg == self.state:
            self.set_new_sprite_values(State.noLeg, self.real_width, self.real_height, 122, 153, self.zombie_sheet_attack_no_leg, 0)

    def set_dead(self):
        self.dead = True
        self.attacking = False
        self.index = 0
        if State.twoLeg == self.state:
            self.set_new_sprite_values(State.twoLeg, self.real_width, self.real_height, 230, 218, self.zombie_sheet_dead_two_leg, 0)
        elif State.oneLeg == self.state:
            self.set_new_sprite_values(State.oneLeg, self.real_width, self.real_height, 230, 206, self.zombie_sheet_dead_one_leg, 0)
        elif State.noLeg == self.state:
            self.set_new_sprite_values(State.noLeg, self.real_width, self.real_height, 173, 176, self.zombie_sheet_dead_no_leg, 0)

    def set_new_sprite_values(self, newState, oldWidth, oldHeight, newWidth, newHeight, newSheet, newSpeed):
        self.state = newState
        self.sheet = newSheet
        self.real_height = newHeight
        self.real_width = newWidth
        if not newSpeed == -1:
            self.speed = newSpeed
        self.calcNewCord([oldWidth, oldHeight], [newWidth, newHeight])
        pass

# fix for the origin problem in pygame, if you change the sprites without calling this function, the sprite "jumps" on screen
    def calcNewCord(self, old, new):
        # self.rect.x += (old[0] - new[0]) / 2
        self.rect.x += (old[0] - new[0]) if (old[0] - new[0]) > 0 else 0
        self.rect.y += (old[1] - new[1])

    def getLayer(self):
        return self.layer


class State(Enum):
    twoLeg = 0
    oneLeg = 1
    noLeg = 2

class HitType(Enum):
    miss = 0
    legshot = 1
    headshot = 2
    chest = 3