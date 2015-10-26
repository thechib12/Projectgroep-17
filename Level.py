from random import randint
import pygame
from Stand import Stand
from Zombie import Zombie

fnt_size = 50
fnt_color = (0, 0, 0)

txt_remaining_pos = (0, 0)
txt_wave_pos = (800, 0)


class Level:
    def __init__(self, i):
        self.count = int(i * 1.5)
        self.wave = 1

        self.font = pygame.font.init()
        self.font = pygame.font.Font("resources/fonts/Lato-Regular.ttf", fnt_size)

        self.txt_remaining = self.font.render("Wave remaining: " + str(self.count), True, fnt_color)
        self.txt_wave = self.font.render("Wave number: " + str(self.wave), True, fnt_color)

        self.enemies = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group()
        self.stand = Stand()
        self.allSprites.add(self.stand)

    def update(self):
        self.enemies.update()
        random = randint(0, 30)
        if self.count > 0 and random == 1:
            self.count -= 1
            self.txt_remaining = self.font.render("Wave remaining: " + str(self.count), True, fnt_color)
            val = (3 - randint(0, 2)) * 200 + 280
            zombie = Zombie(val)
            self.enemies.add(zombie)
            self.allSprites.add(zombie)
        if self.count == 0 and len(self.enemies) == 0:
            self.wave += 1
            self.count = 10 * self.wave
            # TODO betere curve voor zombiespawn
            self.txt_remaining = self.font.render("Wave remaining: " + str(self.count), True, fnt_color)
            self.txt_wave = self.font.render("Wave number: " + str(self.wave), True, fnt_color)

    def getRemaining(self):
        return int(self.count)

    def draw(self, screen):
        # self.enemies.draw(screen)
        self.allSprites.draw(screen)
        screen.blit(self.txt_remaining, txt_remaining_pos)
        screen.blit(self.txt_wave, txt_wave_pos)

    def shoot(self, x, y):
        for enemy in self.enemies:
            if enemy.hit(x, y):
                self.enemies.remove(enemy)
                self.allSprites.remove(enemy)
