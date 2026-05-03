import pygame as pg
from glyph import Glyph
from enum import Enum
from enums import Shader
import math

pg.init()

class ShaderHandler:

    @classmethod
    def shade(cls, items: Glyph | list[Glyph], shaders: Shader | list[Shader], timer) -> None:
        """Apply all passed shaders on all passed items and return sprites of all items"""

        cls.timer = timer

        ### multiple items ###
        if isinstance(items, list):

            for item in items:
                color = pg.Color(0,0,0)

                ### multiple shaders ###
                if isinstance(shaders, list):

                    for shader in shaders:
                        color = cls.__shadeItem(item, shader)

                ### single shader ###
                else:
                    color = cls.__shadeItem(item, shaders)

                item.setColor(color)

        ### single item ###
        else:
            color = pg.Color(0,0,0)

            ### multiple shaders ###
            if isinstance(shaders, list):

                for shader in shaders:
                    color = cls.__shadeItem(items, shader)

            ### single shader ###
            else:
                color = cls.__shadeItem(items, shaders)

            items.setColor(color)

    @classmethod
    def color(cls, items: Glyph | list[Glyph], color: pg.Color) -> None:

        if isinstance(items, list):

            for item in items:

                item.setColor(color)

        else:

            items.setColor(color)

    @classmethod
    def __shadeItem(cls, item: Glyph, shader: Shader) -> pg.Color:
        """calls appropriate shader function on passed item and returns the result"""

        match shader:

            case Shader.RAINBOW:
                color = cls.__rainbow(item)
                return color

            case _:
                color = pg.Color(0,0,0)
                return color

    @classmethod
    def __rainbow(cls, item: Glyph) -> pg.Color:
        """enacts rainbow algorithm over passed item and returns color based on items location"""

        loc = item.location
        outCont = [255, 0, 0]
        steps = math.floor((loc[0] + loc[1] + cls.timer * 4) / 255)
        remaining = (loc[0] + loc[1] + cls.timer * 4) % 255

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

        output = [outCont[0], outCont[1], outCont[2]]

        return pg.Color(*output)