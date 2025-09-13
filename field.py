from glyph import Glyph
from droplet import Droplet
import pygame as pg
import random, string

pg.init()

class Field:
    def __init__(self, width, height, columns, rows):
        self.width = width
        self.height = height
        self.columns = columns
        self.rows = rows
        self.grid = []
        self.cellHeight = int(self.height / self.rows)
        self.cellWidth = int(self.width / self.columns)
        self.glyphSize = int(0.95 * self.cellHeight)
        self.vertMarg = int(0.5 * (self.cellHeight - self.glyphSize))
        self.updated = []
        self.droplets = []

        self.populate()

    def populate(self):
        for column in range(self.columns):
            rowContents = []

            for row in range(self.rows):
                rowContents.append(Glyph(self.cellWidth * column, self.cellHeight * row, self.glyphSize, self))
                print(f"Created glyph #{column + row}")

            self.grid.append(rowContents)

    def newDroplet(self, column):
        self.droplets.append(Droplet(column, random.randint(1,6), self))

    def update(self):
        for droplet in self.droplets:
            droplet.update()

        for column in self.grid:
            for glyph in column:
                if glyph.brightness > 0:
                    glyph.update()
