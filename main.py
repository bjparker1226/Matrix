from unittest import case

import pygame as pg
from win32api import GetSystemMetrics
from glyph import Glyph
from droplet import Droplet
import field, os, random, math

### Declare globals
CLOCK_SPEED = 60
DROPLET_CHECK = pg.event.custom_type()
DROPLET_CHECKRATE = 150

### Get monitor info
MONITOR_WIDTH = GetSystemMetrics(0)
MONITOR_HEIGHT = GetSystemMetrics(1)

### initialize pygame

pg.init()
screen = pg.display.set_mode((MONITOR_WIDTH, MONITOR_HEIGHT))
clock = pg.time.Clock()

### initialize Glyph Field

field = field.Field(MONITOR_WIDTH, MONITOR_HEIGHT, 96, 54)
glyphFont = pg.font.Font('./src/txt/fonts/NaruMonoDemo-Regular.ttf', field.glyphSize)

def rainbowShader(location):
    loc = location
    outCont = [255, 0, 0]
    steps = math.floor((loc[0] + loc[1]) / 255)
    remaining = (loc[0] + loc[1]) % 255

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

    output = (outCont[0], outCont[1], outCont[2])
    # print("Column #%d. %s steps! %s" % (location[0], steps, str(output)))

    if loc[0] == 765:
        pass

    return output


if __name__ == '__main__':

    pg.time.set_timer(DROPLET_CHECK, DROPLET_CHECKRATE)

    running = True

    tempGlyphColor = (255,255,255,255)

    while running:

        field.updated = []

        # list of items to be rendered to the screen
        toBlit = []

        # poll for events


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

            elif event.type == DROPLET_CHECK:
                if random.randint(0,9) > 5:
                    # tempGlyphColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    field.newDroplet(random.randint(0,field.columns-1))
                    pg.event.clear(DROPLET_CHECK)
                    print("New droplet!")

        field.update()

        # for glyph in field.updated:
        #         color = glyph.renderColor
        #         toBlit.append([glyphFont.render(glyph.char, True, color), glyph.blitLoc()])

        # wipe screen
        screen.fill((0,0,0))

        pxarray = pg.PixelArray(screen)
        for column in range(len(pxarray)):
            for row in range(len(pxarray[column])):
                color = rainbowShader((column, row))
                pxarray[column][row] = color

        toBlit.append(pxarray.make_surface())
        pxarray.close()

        # update screen

        for sprite in toBlit:
            # screen.blit(sprite[0],sprite[1])
            screen.blit(sprite, (0,0))

        pg.display.update()

        clock.tick(CLOCK_SPEED)

    pg.quit()
