import pygame as pg
from glyph import Glyph
import math

pg.init()

class ShaderHandler:

    @classmethod
    def shade(cls, items: Glyph | list[Glyph], shaders: str | list[str], timer) -> None:
        """Enact all passed shaders on all passed items"""

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

    @classmethod
    def __shadeItem(cls, item: Glyph, shader: str) -> pg.Color:
        match shader:
            case "rainbow":
                return cls.__rainbow(item)

    @classmethod
    def __rainbow(cls, item: Glyph) -> pg.Color:
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
