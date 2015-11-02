import threading
from time import sleep
import pygame

__author__ = 'reneb_000'


class Cursor(pygame.sprite.Sprite, threading.Thread):
    def __init__(self, lockobj):
        # init pygame sprite class
        super().__init__()
        threading.Thread.__init__(self)

        self.lock = lockobj
        self.pos_toset = [0, 0]
        # set the image of the object
        self.image = pygame.image.load("resources/images/crosshairs/crosshair0.png").convert_alpha()
        self.sound = pygame.mixer.Sound("resources/sounds/pistol.ogg")
        # self.image.fill([0, 0, 0])
        self.rect = self.image.get_rect()
        self.shot = False
        self.recoil = 0

    def run(self):
        while True:
            # next line get for the position
            pos = pygame.mouse.get_pos()
            self.set_pos_toset(pos)
            sleep(0.05)
        pass

    def setXY(self, x, y):
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2 - self.recoil

    def set_pos_toset(self, tupel):
        self.lock.acquire()
        self.pos_toset = tupel
        self.lock.release()

    def getXY(self):
        """
        self.lock.acquire()
        pos = pygame.mouse.get_pos()
        val = [pos[0], pos[1] - self.recoil]
        self.lock.release()
        """
        # return val
        return [self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2 + self.recoil]

    def update(self):
        # pos = pygame.mouse.get_pos()
        self.lock.acquire()
        # self.setXY(pos[0], pos[1])
        self.setXY(self.pos_toset[0], self.pos_toset[1])
        self.lock.release()
        if self.shot and self.recoil >= 6:
            self.recoil -= 6
        else:
            self.recoil = 0
            self.shot = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def shoot(self):
        self.sound.play()
        self.shot = True
        self.recoil += 100

    def set_image(self, image):
        self.image = image


