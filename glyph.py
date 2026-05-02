import pygame as pg
import string, random

pg.init()

class Glyph:
    def __init__(self, x: int, y: int, fontSize: int, parent) -> None:
        self.char = '0'
        self.brightness = 0
        self.transparency = 255
        self.location = (x, y)
        self.fontSize = int(fontSize)
        self.fontPath = './src/txt/fonts/Matrix.ttf'
        self.font = pg.font.Font(self.fontPath, self.fontSize)
        self.parent = parent

        self.vertMarg = parent.vertMarg
        self.horMarg = 0
        self.trueColor = (255,255,255)
        self.renderColor = self.trueColor
        self.pingDuration = 0
        self.flashSpeed = 0


    def update(self):

        self.char = random.choice(string.ascii_letters)

        if self.brightness > 255:
            self.brightness -= 2

        self.brightness -= 2
        if self.brightness < 0:
            self.brightness = 0

        if self.brightness < self.transparency:
            self.transparency = self.brightness


    def blitLoc(self) -> tuple[int,int]:
        return (self.location[0] + self.horMarg, self.location[1] + self.vertMarg)


    def ping(self, duration: int) -> None:
        self.pingDuration = duration
        self.flashSpeed = duration
        self.transparency = 255

    def draw(self) -> pg.Surface:
        """Return surface object for blitting"""
        self.__factorBrightness()
        returnSurf = self.font.render(self.char, True, self.renderColor)
        returnSurf.set_alpha(self.transparency)
        return returnSurf

    def rect(self) -> pg.Rect:
        """Return rect object for screen updating"""
        rect = pg.Rect(*self.blitLoc(), self.parent.cellWidth, self.parent.cellHeight)
        return rect

    def setColor(self, color: pg.Color) -> None:
        self.trueColor = color

    def __factorBrightness(self) -> None:
        if self.brightness > 255:
            ovrBrightness = self.brightness- 256
            r = self.trueColor[0]+(255 - self.trueColor[0])*(ovrBrightness)/255
            g = self.trueColor[1]+(255 - self.trueColor[1])*(ovrBrightness)/255
            b = self.trueColor[2]+(255 - self.trueColor[2])*(ovrBrightness)/255
            self.renderColor = (r,g,b)
