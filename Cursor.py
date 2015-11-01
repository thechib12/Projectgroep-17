import pygame

__author__ = 'reneb_000'


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        # init pygame sprite class
        super().__init__()
        # set the image of the object
        self.image = pygame.image.load("resources/images/crosshairs/crosshair0.png").convert_alpha()
        self.sound = pygame.mixer.Sound("resources/sounds/pistol.ogg")
        # self.image.fill([0, 0, 0])
        self.rect = self.image.get_rect()
        self.shot = False
        self.recoil = 0

    def setXY(self, x, y):
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2 - self.recoil

    def getXY(self):
        pos = pygame.mouse.get_pos()
        return [pos[0], pos[1] - self.recoil]

    def update(self):
        pos = pygame.mouse.get_pos()
        self.setXY(pos[0], pos[1])
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


