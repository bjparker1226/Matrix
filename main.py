from unittest import case

import pygame as pg
from win32api import GetSystemMetrics

import shaderhandler
from shaderhandler import ShaderHandler
from enums import Shader
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
# glyphFont = pg.font.Font('./src/txt/fonts/NaruMonoDemo-Regular.ttf', field.glyphSize)

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
                if random.randint(0,9) > 6:
                    field.newDroplet(random.randint(0,field.columns-1))
                    pg.event.clear(DROPLET_CHECK)

        field.update()

        # ShaderHandler.shade(field.updated,Shader.RAINBOW,timer)
        ShaderHandler.color(field.updated, pg.Color(0,255,0))

        for glyph in field.updated:
            toBlit.append((glyph.draw(),glyph.blitLoc()))
            toUpdate.append(glyph.rect())


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
