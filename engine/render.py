import copy
import sys

import constants as cfg
from . import (colours, bitmasks)


class Renderer:

    def __init__(self, width, height, background_colour=cfg.BACKGROUND_COLOUR):
        self.width = width
        self.height = height
        self.screen = ANSIIScreen(width, height)
        self.background_colour = background_colour
        self.buffer = [[self.background_colour for y in range(self.height)] \
                       for x in range(self.width)]
        # set every pixel in ref_buffer to impossible value so that it gets
        # completely rerendered
        self.ref_buffer = [[-1 for y in range(height)] \
                           for x in range(width)]
        self.rerender()

    def draw_pixel(self, x, y, colour):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[int(x)][int(y)] = colour

    def draw_string(self, string, x, y, colour, centered=False):
        if centered:
            width = self.get_label_width(string)
            x -= width / 2
        for c in string:
            bitmask = bitmasks.CHARS[c]
            self.draw_bitmask(x, y, bitmask, colour)
            # advance to the position of the next character
            x += len(bitmask[0]) + 1

    def draw_bitmask(self, x, y, bitmask, colour):
        # note that the order of the loops is 'swapped' (dy in outer loop
        # and dx in inner loop). This allows the bitmasks to be created more
        # easily as they don't have to be transposed (see ./bitmasks.py) .
        for dy, row in enumerate(bitmask):
            for dx, b in enumerate(row):
                if b:
                    self.draw_pixel(x + dx, y + dy, colour)


    def get_label_width(self, string):
        """returns the width in pixels that a string would use if drawn to the
        screen"""
        width = 0
        for c in string:
            bitmask = bitmasks.CHARS[c]
            width += len(bitmask[0]) + 1
        return width

    def rerender(self):
        # to change as few pixels on the screen as possible, the renderer has
        # two buffers storing each pixel on the screen, one of the current
        # frame ('ref_buffer') and one of the next frame ('buffer'). When
        # rerender is called, only the pixels that actually differ get updated.
        changes = []
        for x, (buff_column, ref_column) in enumerate(zip(self.buffer,
                                                          self.ref_buffer)):
            for y, (buff_pix, ref_pix) in enumerate(zip(buff_column,
                                                        ref_column)):
                if buff_pix != ref_pix:
                    changes.append({'x': x,
                                    'y': y,
                                    'colour': buff_pix})
                    # incrementally change ref_buffer so that it matches the buffer
                    # by the end of rerender.
                    self.ref_buffer[x][y] = buff_pix
                self.buffer[x][y] = self.background_colour
        self.screen.update(changes)


def move_cursor(x, y):
    print("\033[%d;%df" % (y + 1, x + 1), end="")

class ANSIIScreen:
    """An interface for the renderer to operate with ANSII escape codes. Helps
    to keep the program modular and pluggable as the renderer itself does not
    need to know the specifics of the canvas it is actually rendering to. (This
    could also be an interface to any other kind of screen. It only needs to
    have an 'update' method similar to the one below)"""
    # http://ascii-table.com/ansi-escape-sequences.php

    _ANSII_COLOUR_VALUES = {
        colours.BLACK:   40,
        colours.RED:     41,
        colours.GREEN:   42,
        colours.YELLOW:  43,
        colours.BLUE:    44,
        colours.MAGENTA: 45,
        colours.CYAN:    46,
        colours.WHITE:   47,
    }

    def __init__(self, width, height, output=cfg.ANSIISCREEN_OUTPUT):
        self._output = output
        self.width = width
        self.height = height
        # clear screen
        self._output("\033[2J")
        # set screen dimensions
        self._output("\033[=3h")
        # hide cursor
        self._output("\033[?25l")

    def __del__(self):
        self._move_cursor(self.height + 2, 0)

    def update(self, changes):
        # applies all changes to the screen by sending ASCII escape codes to
        # the _output
        for command in changes:
            x = command['x']
            y = command['y']
            if 0 <= x < self.width and 0 <= y < self.height:
                self._move_cursor(x, y)
                self._set_colour(command['colour'])
        # this is specific to when _output is the default python 'print'
        sys.stdout.flush()

    def _move_cursor(self, x, y):
        self._output("\033[%d;%df" % (y + 1, x + 1))

    def _set_colour(self, colour, c=" "):
        # c is the character that is actually prited, usually a space if we only
        # want to set the colour of the pixel
        self._output("\u001b[%dm%s\u001b[0m" % (
            self._ANSII_COLOUR_VALUES[colour], c))
