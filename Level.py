from random import randint


class Level:
    def __init__(self, i):
        self.count = 0
        self.count = i * 1.5

    def update(self):
        random = randint(0, 60)
        if self.count > 0 and random == 1:
            self.count -= 1
            val = (3 - randint(0, 3)) * 200
            return val
        return -1

    def getRemaining(self):
        return int(self.count)
