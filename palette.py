from collections import deque

import pygame

from cycle import Cycle

pcolumns = 13
prows = 20
psize = 16
pmargin = 5
pwidth = ((psize + pmargin) * pcolumns) + pmargin
pheight = ((psize + pmargin) * prows) + pmargin

# NOTE(m): This magic number comes from the original Deluxe Paint source code
# file CCYCLE.C line number 19
# The division by two comes from our FPS of 30, which is half of 60 fps,
# the modern LCD equivalent of 60 Hz on an old school CRT.
# This seems to most accurately recreate the speed as measured in Deluxe Paint
# in DOSBox.
ONE_PER_TICK = 16384 / 2


class Palette:
    def __init__(self, colors, cycles):
        self.colors = [tuple(color) for color in colors]
        self.basecolors = [color for color in self.colors]
        self.surface = pygame.Surface((pwidth, pheight), 0, 8)
        self.surface.set_palette(self.colors)

        # Process cycles
        self.cycles = [Cycle(cycle['rate'],
                             cycle['reverse'],
                             cycle['low'],
                             cycle['high'])
                       for cycle in cycles
                       if cycle['rate'] > 0]

        for index in range(256):
            rownumber = int(index / pcolumns)
            colnumber = index % pcolumns
            destrect = pygame.Rect(0, 0, psize, psize)

            pygame.draw.rect(
                self.surface,
                index,
                destrect.move(pmargin + (colnumber * (psize + pmargin)),
                              (pmargin + rownumber * (psize + pmargin)))
            )

    def cycle(self):
        for cycle in self.cycles:
            cycle.count += cycle.rate
            if cycle.count >= ONE_PER_TICK:
                cycle.count -= ONE_PER_TICK
                cyclecolors = deque(self.colors[cycle.low:cycle.high + 1])
                if cycle.reverse == 2:
                    cyclecolors.rotate(-1)
                else:
                    cyclecolors.rotate(1)
                self.colors[cycle.low:cycle.high + 1] = cyclecolors
