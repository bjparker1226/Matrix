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
        self.trueColor = ((255,255,255))
        self.renderColor = self.trueColor
        self.pingDuration = 0
        self.flashSpeed = 0


    def update(self):

        self.char = random.choice(string.ascii_uppercase)

        self.brightness -= 1

        # self.updateColor()


    def blitLoc(self):
        return (self.location[0] + self.horMarg, self.location[1] + self.vertMarg)


    def ping(self, duration):
        self.pingDuration = duration
        self.flashSpeed = duration
        self.brightness = 255

    def setBrightness(self, brightness):
        self.brightness = brightness
