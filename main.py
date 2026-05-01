from unittest import case

import pygame as pg
from win32api import GetSystemMetrics
from glyph import Glyph
from droplet import Droplet
import field, os, random, math

"""
Declare globals
"""

CLOCK_SPEED = 60
DROPLET_CHECK = pg.event.custom_type()
DROPLET_CHECKRATE = 150

### Get monitor info
MONITOR_WIDTH = GetSystemMetrics(0)
MONITOR_HEIGHT = GetSystemMetrics(1)


### initialize pygame ###

pg.init()
screen = pg.display.set_mode((MONITOR_WIDTH, MONITOR_HEIGHT))
clock = pg.time.Clock()

### initialize Glyph Field ###

field = field.Field(MONITOR_WIDTH, MONITOR_HEIGHT, 96, 54)
glyphFont = pg.font.Font('./src/txt/fonts/NaruMonoDemo-Regular.ttf', field.glyphSize)

def main():

    """
    custom events
    """
    pg.time.set_timer(DROPLET_CHECK, DROPLET_CHECKRATE)



    running = True

    tempGlyphColor = (255,255,255,255)

    timer = 0

    while running:

        field.updated = []

        toBlit = [] # list of items to be rendered to the screen
        toUpdate = [] # list of rects to be updated on screen

        # poll for events

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

            elif event.type == DROPLET_CHECK and clock.get_fps() >= CLOCK_SPEED*0.8:
                if random.randint(0,9) > 5:
                    field.newDroplet(random.randint(0,field.columns-1))
                    pg.event.clear(DROPLET_CHECK)

        field.update()

        glyphs = []

        for glyph in field.updated:
            if glyph.brightness > 0:
                color = rainbowShader(glyph.blitLoc(),timer)
                # glyphs.append([glyphFont.render(glyph.char, True, color), glyph.blitLoc()])
                toBlit.append((glyphFont.render(glyph.char, True, color),glyph.blitLoc()))
            toUpdate.append(pg.Rect(glyph.blitLoc()[0], glyph.blitLoc()[1], field.cellWidth, field.cellHeight))

        # for glyph in glyphs:
        #     pxarray = pg.PixelArray(glyph[0])
        #     color = rainbowShader((glyph[1][0], glyph[1][1]),timer)
        #     for column in range(len(pxarray)):
        #         for row in range(len(pxarray[column])):
        #             if not pxarray[column][row] == 16777215:
        #                 pxarray[column][row] = color
        #
        #     glyphSurf = pxarray.make_surface()
        #     toBlit.append((glyphSurf,glyph[1]))
        #
        #     pxarray.close()

        # wipe screen
        screen.fill((0,0,0))

        """
        FPS counter
        """

        boxSize = (0.05*MONITOR_WIDTH,0.05*MONITOR_HEIGHT)
        boxBuffer = int(0.025*MONITOR_WIDTH)
        counterBox = fpsBox(clock.get_fps(),boxSize)
        toBlit.append((counterBox,(boxBuffer,boxBuffer)))
        toUpdate.append(counterBox.get_rect(left=boxBuffer, top=boxBuffer))

        """
        update screen
        """

        for sprite in toBlit:
            screen.blit(sprite[0],sprite[1])
            # screen.blit(sprite, (0,0))

        # pg.display.update()
        pg.display.update(toUpdate)

        clock.tick(CLOCK_SPEED)
        timer += 2

    pg.quit()

def rainbowShader(location, timer):
    loc = location
    outCont = [255, 0, 0]
    steps = math.floor((loc[0] + loc[1] + timer * 4) / 255)
    remaining = (loc[0] + loc[1] + timer * 4) % 255

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

def fpsBox(fps, size):

    returnSurf = pg.Surface(size) # create surface to be returned
    returnSurf.fill((0,0,0))
    pg.draw.rect(returnSurf,(255,255,255),(0,0,size[0],size[1]),2) # draw border to return surface

    fpsCount = trunc(fps,2)
    fpsFont = pg.font.SysFont('Arial', int(size[1]/3))
    fpsText = fpsFont.render(str(fpsCount),True,(255,255,255))

    returnSurf.blit(fpsText,((size[0]-fpsText.get_size()[0])/2,(size[1]-fpsText.get_size()[1])/2))

    return returnSurf


def trunc(number, decimals):
    before,after = str(number).split(".")
    return f"{before}.{after[:decimals]}fps"

if __name__ == "__main__":
    main()
