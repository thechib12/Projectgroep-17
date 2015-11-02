import json

__author__ = 'reneb_000'

class Settings():
    bloodspawn = False
    play_audio = False


class SharedPreference():

    def __init__(self):
        self.file = open("data.rene", "r")
        self.json = json.load(self.file)
        self.file.close()

    def loadHighscore(self, name, default):
        try:
            return self.json['highscore'][name]
        except KeyError:
            return default

    def writeHighscore(self, name, value):
        try:
            if value > self.json['highscore'][name]:
                self.json['highscore'][name] = value
        except TypeError:
            if self.timebigger(value, name):
                self.json['highscore'][name] = str(value)

    def timebigger(self, value, name):
        ar1 = str(value).split(":")
        ar2 = self.json['highscore'][name].split(":")
        for i in range(0, len(ar1)):
                if int(ar1[i]) < int(ar2[i]):
                    return False
        return True


    def commit(self):
        try:
            self.file = open("data.rene", "w")
            json.dump(self.json, self.file)
            self.file.close()
        except IOError:
            print("Could not commit")


"""
test = SharedPreference()
print(test.loadHighscore("game_wave", -1))
test.writeHighscore("game_wave", 100)
print(test.loadHighscore("game_wave", -1))
test.commit()
"""




"""
with open('data.rene', 'r') as outfile:
    #json.dump("{test: 1}", outfile)
    test = json.load(outfile)
    # test2 = json.loads(test)
    print(test['testd'])
"""