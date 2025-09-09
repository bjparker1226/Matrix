import pygame as pg
import string, random

pg.init()

class Glyph:
    def __init__(self, x, y, fontSize, parent):
        self.char = '0'
        self.brightness = 0
        self.location = (x, y)
        self.fontSize = int(fontSize)
        self.fontPath = './src/txt/fonts/NaruMonoDemo-Regular.ttf'
        self.parent = parent

        kawi_pink = (255, 5, 109)
        tropical_ocean = (0, 255, 208)

        self.vertMarg = parent.vertMarg
        self.horMarg = 0
        self.trueColor = (kawi_pink)
        self.renderColor = self.trueColor
        self.pingDuration = 0
        self.flashSpeed = 0


    def update(self):

        self.char = random.choice(string.ascii_uppercase)

        self.brightness -= 1

        self.updateColor()

        self.parent.updated.append(self)


    def blitLoc(self):
        return (self.location[0] + self.horMarg, self.location[1] + self.vertMarg)

    def updateColor(self):
        newColor = [self.trueColor[0], self.trueColor[1], self.trueColor[2]]

        if self.pingDuration > 0:
            self.brightness = 255
            for val in range(len(newColor)):
                newColor[val] += self.pingDuration * (255 - self.trueColor[val]) * (1/self.flashSpeed)
            self.pingDuration -= 1

        else:
            for val in range(len(self.trueColor)):
                if newColor[val] > self.brightness:
                    newColor[val] = self.brightness
                else:
                    newColor[val] = self.trueColor[val]

        for value in range(len(newColor)):
            if newColor[value] < 0:
                newColor[value] = 0
            if newColor[value] > 255:
                newColor[value] = 255

        self.renderColor = (newColor[0], newColor[1], newColor[2])

    def ping(self, duration):
        self.pingDuration = duration
        self.flashSpeed = duration
        self.brightness = 255

    def setBrightness(self, brightness):
        self.brightness = brightness
