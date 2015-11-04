import threading
from time import sleep
import pygame
# from ShootObject import ShootObj

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

        self.toshoot = False
        # self.shoot_obj = ShootObj()
        self.shoot_lock = threading.Lock()

        self.getter = xyGetter(self)
        self.getter.start()

        self.buttongetter = ButtonGetter(self)

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
        if self.toshoot:
            self.shoot_lock.acquire()
            self.toshoot = False
            self.shoot_lock.release()
            # self.shoot_obj.shootMain()
            import Main
            Main.shoot()
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

    def calibrate(self):
        self.getter.calibrate()

    def set_to_shoot(self):
        self.shoot_lock.acquire()
        self.toshoot = True
        self.shoot_lock.release()



import smbus
import math
import time

class xyGetter(threading.Thread):

    def __init__(self, cursor):
        threading.Thread.__init__(self)
        self.cursor = cursor
        self.lock = threading.Lock()

        # Power management registers
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c

        self.gyro_scale = 131.0
        self.accel_scale = 16384.0

        self.address = 0x68  # This is the address value read via the i2cdetect command

        self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards

        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

        self.now = time.time()

        self.K = 0.98
        self.K1 = 1 - self.K

        self.time_diff = 0.01

        (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.read_all()

        self.last_x = self.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        # self.last_y = self.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        self.last_y = self.get_z_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

        self.gyro_offset_x = gyro_scaled_x
        # self.gyro_offset_y = gyro_scaled_y
        self.gyro_offset_y = gyro_scaled_z

        self.gyro_total_x = (self.last_x) - self.gyro_offset_x
        self.gyro_total_y = (self.last_y) - self.gyro_offset_y

        self.gyro_sample = 1/8000

        self.calx = self.last_x
        self.caly = self.last_y

        # print("{0:.4f} {1:.2f} {2:.2f} {3:.2f} {4:.2f} {5:.2f} {6:.2f}".format( time.time() - now, (last_x), gyro_total_x, (last_x), (last_y), gyro_total_y, (last_y)))
        # TODO PRINT SHIT


    def calibrate(self):
        self.lock.acquire()
        self.calx = self.last_x
        self.caly = self.last_y
        self.lock.release()

    def run(self):
        # for i in range(0, int(3.0 / self.time_diff)):
        while True:
            time.sleep(self.time_diff - 0.005)

            (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.read_all()

            gyro_scaled_x -= self.gyro_offset_x
            # gyro_scaled_y -= self.gyro_offset_y
            gyro_scaled_z -= self.gyro_offset_y

            # gyro_x_delta = (gyro_scaled_x * self.time_diff)
            gyro_x_delta = (gyro_scaled_x * self.gyro_sample)
            # gyro_y_delta = (gyro_scaled_y * self.time_diff)
            gyro_y_delta = (gyro_scaled_z * self.time_diff)

            self.gyro_total_x += gyro_x_delta
            self.gyro_total_y += gyro_y_delta

            rotation_x = self.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
            # rotation_y = self.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
            rotation_y = self.get_z_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)


            self.lock.acquire()
            # self.last_x = self.K * (self.last_x + gyro_x_delta) + (self.K1 * rotation_x)
            self.last_x = self.gyro_total_x
            self.last_y = self.K * (self.last_y + gyro_y_delta) + (self.K1 * rotation_y)

            # print "{0:.4f} {1:.2f} {2:.2f} {3:.2f} {4:.2f} {5:.2f} {6:.2f}".format( time.time() - now, (rotation_x), (gyro_total_x), (last_x), (rotation_y), (gyro_total_y), (last_y))

            calibrated_x = self.last_x - self.calx
            calibrated_y = self.last_y - self.caly

            x = 960 + math.tan(math.radians(calibrated_x*100)) * 1080
            y = 540 + math.tan(math.radians(calibrated_y)) * 1080
            # print("{0:.2f} {1:.2f} {2:.2f} {3:.2f}".format(self.last_x, self.last_y, calibrated_x, calibrated_y))
            self.lock.release()
            self.cursor.set_pos_toset([x, y])


        pass





    def read_all(self):
        raw_gyro_data = self.bus.read_i2c_block_data(self.address, 0x43, 6)
        raw_accel_data = self.bus.read_i2c_block_data(self.address, 0x3b, 6)

        gyro_scaled_x = self.twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.gyro_scale
        gyro_scaled_y = self.twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.gyro_scale
        gyro_scaled_z = self.twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.gyro_scale

        accel_scaled_x = self.twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / self.accel_scale
        accel_scaled_y = self.twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / self.accel_scale
        accel_scaled_z = self.twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / self.accel_scale

        return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z)

    def twos_compliment(self, val):
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))


    def get_y_rotation(self, x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self, x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)

    def get_z_rotation(self, x,y,z):
        radians = math.atan2(self.dist(x,y), z)
        return math.degrees(radians)


import wiringpi2 as wiringpi


class ButtonGetter(threading.Thread):

    def __init__(self, cursor):
        threading.Thread.__init__(self)
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(17, 0)
        self.cursor = cursor
        self.start()

    def run(self):
        while True:
            time.sleep(0.01)
            if wiringpi.digitalRead(17) > 0:
                self.cursor.set_to_shoot()