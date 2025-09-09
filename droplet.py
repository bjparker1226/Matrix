import pygame as pg
import random, math

pg.init()

class Droplet:
    def __init__(self, column, speed, parent):
        self.column = column
        self.speed = speed
        self.currentGlyph = parent.grid[column][0]
        self.ypos = 0
        self.parent = parent
        self.pingDuration = 60
        self.pingedGlyphs = []

    def update(self):
        self.ypos += self.speed
        if math.trunc(self.ypos / self.parent.cellHeight) < self.parent.rows and self.ypos < self.parent.height:
            self.currentGlyph = self.parent.grid[self.column][math.trunc(self.ypos / self.parent.cellHeight)]
            if self.currentGlyph not in self.pingedGlyphs:
                self.currentGlyph.ping(math.trunc(self.pingDuration))
                self.pingedGlyphs.append(self.currentGlyph)

        else:
            self.parent.droplets.remove(self)