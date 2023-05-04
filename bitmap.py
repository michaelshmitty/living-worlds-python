import json

import pygame

from palette import Palette


class Bitmap:
    def __init__(self, filepath):
        with open(filepath,) as jsonfile:
            image = json.load(jsonfile)

        self.filename = image['filename']
        self.width = image['width']
        self.height = image['height']
        self.pixels = image['pixels']
        self.palette = Palette(image['colors'], image['cycles'])
        self.surface = pygame.Surface((self.width, self.height), 0, 8)
        self.surface.set_palette(self.palette.colors)

        # Load image onto surface
        with pygame.PixelArray(self.surface) as pixels:
            for x in range(self.width):
                for y in range(self.height):
                    offset = x + (y * self.width)
                    pixels[x, y] = self.pixels[offset]
