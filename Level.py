from random import randint
import pygame
from Stand import Stand
from Zombie import Zombie

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

        self.font = pygame.font.init()
        self.font = pygame.font.Font("resources/fonts/Lato-Regular.ttf", fnt_size)

        self.txt_remaining = self.font.render("Wave remaining: " + str(self.count), True, fnt_color)
        self.txt_wave = self.font.render("Wave number: " + str(self.wave), True, fnt_color)
        self.txt_health = self.font.render("Health: ", True, fnt_color)

        self.stand = Stand()
        self.enemies = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
        self.stand = pygame.sprite.GroupSingle(self.stand)
        self.stains = pygame.sprite.Group()

    def update(self):
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

    def shoot(self, x, y):
        for i in [self.enemies[2], self.enemies[1], self.enemies[0]]:
            for enemy in i:
                if enemy.hit(x, y):
                    # self.enemies[enemy.getLayer()].remove(enemy)
                    self.stains.add(BloodStain(self))
                    return
                    # self.allSprites.remove(enemy)

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
        pygame.draw.line(screen, (0, 255, 0), [1600, 30], [1600 + (1900-1600)*self.health/self.health_max, 30], 45)

    def decrease_health(self, value):
        if self.health - value <= 0:
            self.health = 0
        else:
            self.health -= value

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
