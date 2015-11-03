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

        self.getter = xyGetter(self)
        self.getter.start()

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
        # return [self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2 + self.recoil]
        return [self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2]

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


""" getting date from sensor """
import smbus
import math
import time


def twos_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)


def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


def read_all(bus, address, gyro_scale, accel_scale):
    raw_gyro_data = bus.read_i2c_block_data(address, 0x43, 6)
    raw_accel_data = bus.read_i2c_block_data(address, 0x3b, 6)

    gyro_scaled_x = twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / gyro_scale
    gyro_scaled_y = twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / gyro_scale
    gyro_scaled_z = twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / gyro_scale

    accel_scaled_x = twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / accel_scale
    accel_scaled_y = twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / accel_scale
    accel_scaled_z = twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / accel_scale

    return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z)


class xyGetter(threading.Thread):

    # Power management registers
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c

    gyro_scale = 131.0
    accel_scale = 16384.0

    address = 0x68  # This is the address value read via the i2cdetect command

    bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards

    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)

    now = time.time()

    K = 0.98
    K1 = 1 - K

    # error may happen here in time_diff assigning
    time_diff = 0.01


    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all(bus, address, gyro_scale, accel_scale)

    last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    beginx = last_x
    beginy = last_y

    gyro_offset_x = gyro_scaled_x
    gyro_offset_y = gyro_scaled_y

    gyro_total_x = (last_x) - gyro_offset_x
    gyro_total_y = (last_y) - gyro_offset_y

    gyro_sample_rate = 1/8000

    def __init__(self, cursor):
        threading.Thread.__init__(self)
        self.cursor = cursor

    def run(self):
        while True:
            time.sleep(self.time_diff - 0.005)

            (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all(self.bus, self.address, self.gyro_scale, self.accel_scale)

            gyro_scaled_x -= self.gyro_offset_x
            gyro_scaled_y -= self.gyro_offset_y

            # gyro_x_delta = (gyro_scaled_x * self.time_diff)
            gyro_x_delta = (gyro_scaled_x * self.gyro_sample_rate)
            gyro_y_delta = (gyro_scaled_y * self.time_diff)

            self.gyro_total_x += gyro_x_delta
            self.gyro_total_y += gyro_y_delta

            rotation_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
            rotation_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

            # self.last_x = self.K * (self.last_x + gyro_x_delta) + (self.K1 * rotation_x)
            self.last_x = (self.last_x + gyro_x_delta)
            self.last_y = self.K * (self.last_y + gyro_y_delta) + (self.K1 * rotation_y)

            """"
            if self.last_y < 0 :
                self.last_y = 0
            elif self.last_y > 45:
                self.last_y = 45
            """
            lx = self.last_x-self.beginx
            ly = self.last_y-self.beginy
            len = math.tan(math.radians(ly))*1080
            y = len - (math.cos(math.radians(math.fabs(lx)))*len)
            #x = 960 + len * math.sin(math.radians(lx))
            x = 960
            self.cursor.set_pos_toset([x, y])

            print("{0:.2f} {1:.2f} {2:.2f} {2:.2f}".format(lx, ly, x, y))


