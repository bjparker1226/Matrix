import pygame as pg
import math, glyph

pg.init()

class ShaderHandler:
    def __init__(self):
        self.counter = 0
        self.spritesIn = []
        self.spritesOut = []

    def shade(self):

         for glyph in self.spritesIn:
             self.rainbow(glyph.sprite, glyph.blitLoc(), glyph.brightness, glyph)

         return self.spritesOut


    def addSprite(self, input):

        match type(input):
            case glyph.Glyph:
                self.spritesIn.append(input)
            case List:
                for sprite in input:
                    self.spritesIn.append(sprite)


    def update(self):
        self.counter += 1
        self.spritesIn = []
        self.spritesOut = []

    def rainbow(self, sprite, location, opacity, parent):
        pxArray = pg.PixelArray(sprite)


        for x in range(pxArray.shape[0]):
            for y in range(pxArray.shape[1]):
                if pxArray[x, y] != 0:
                    loc = location + (x, y)

                    outCont = [255, 0, 0, opacity]
                    steps = math.floor((loc[0] + loc[1] + self.counter * 4) / 255)
                    remaining = (loc[0] + loc[1] + self.counter * 4) % 255

                    match steps % 6:
                        case 0:
                            outCont[1] += remaining
                        case 1:
                            outCont[0] -= remaining
                            outCont[1] = 255
                        case 2:
                            outCont[0] = 0
                            outCont[1] = 255
                            outCont[2] += remaining
                        case 3:
                            outCont[0] = 0
                            outCont[1] = 255 - remaining
                            outCont[2] = 255

                        case 4:
                            outCont[0] = 0 + remaining
                            outCont[1] = 0
                            outCont[2] = 255
                        case 5:
                            outCont[0] = 255
                            outCont[1] = 0
                            outCont[2] = 255 - remaining

                    pxArray[x, y] = (outCont[0], outCont[1], outCont[2], outCont[3])
        self.spritesOut.append([pxArray.make_surface(), parent.blitLoc()])