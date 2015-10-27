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

        self.stand = Stand()
        self.enemies = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
        self.stand = pygame.sprite.GroupSingle(self.stand)

    def update(self):
        self.update_enemies()
        random = randint(0, 30)
        if self.count > 0 and random == 1:
            self.count -= 1
            self.txt_remaining = self.font.render("Wave remaining: " + str(self.count), True, fnt_color)
            rand = randint(0, 2)
            val = rand * 130 + 500
            zombie = Zombie(val, rand)
            self.enemies[rand].add(zombie)
        if self.count == 0 and self.no_enemies_left():
            self.wave += 1
            self.count = 10 * self.wave
            # TODO betere curve voor zombiespawn
            self.txt_remaining = self.font.render("Wave remaining: " + str(self.count), True, fnt_color)
            self.txt_wave = self.font.render("Wave number: " + str(self.wave), True, fnt_color)

    def getRemaining(self):
        return int(self.count)

    def draw(self, screen):
        self.stand.draw(screen)
        self.draw_enemies(screen)
        screen.blit(self.txt_remaining, txt_remaining_pos)
        screen.blit(self.txt_wave, txt_wave_pos)

    def shoot(self, x, y):
        for i in [self.enemies[2], self.enemies[1], self.enemies[0]]:
            for enemy in i:
                if enemy.hit(x, y):
                    self.enemies[enemy.getLayer()].remove(enemy)
                    return
                    # self.allSprites.remove(enemy)

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
