#!/usr/bin/env python

import os
from collections import deque

import pygame
from pygame.locals import USEREVENT
import psutil

from bitmap import Bitmap

FPS = 30
FULLSCREEN = False

WIDTH = 1280
HEIGHT = 800
SCALE_WIDTH = 1064
SCALE_HEIGHT = 798

pygame.init()
if FULLSCREEN:
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()
pygame.display.set_caption('Mark J. Ferrari tribute')
clock = pygame.time.Clock()
font = pygame.font.SysFont('bitstreamverasansmono', 14)
UPDATE_STATS = USEREVENT + 1
pygame.time.set_timer(UPDATE_STATS, 1000)

# Load scenes
filenames = os.listdir('scenes/')
filenames.sort()
scenes = deque([f'scenes/{filename}' for filename in filenames
                if filename != 'TESTRAMP.json'])
bitmap = Bitmap(scenes[0])
bitmap_rect = bitmap.surface.get_rect()
bitmap_rect.center = screen_rect.center
pygame.display.set_caption(f'Mark J. Ferrari tribute - {bitmap.filename}')

showpalette = False
cycling = True
running = True
cpu_percent = psutil.cpu_percent()
mem_percent = psutil.virtual_memory().percent

while running:
    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == UPDATE_STATS:
            if showpalette:
                cpu_percent = psutil.cpu_percent()
                mem_percent = psutil.virtual_memory().percent
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cycling = not cycling
            elif event.key == pygame.K_LEFT:
                scenes.rotate(1)
                bitmap = Bitmap(scenes[0])
                pygame.display.set_caption(
                    f'Living Worlds - {bitmap.filename}')
            elif event.key == pygame.K_RIGHT:
                scenes.rotate(-1)
                bitmap = Bitmap(scenes[0])
                pygame.display.set_caption(
                    f'Living Worlds - {bitmap.filename}')
            elif event.key == pygame.K_p:
                showpalette = not showpalette
            else:
                running = False

    # Update
    if cycling:
        bitmap.palette.cycle()
        bitmap.surface.set_palette(bitmap.palette.colors)

    # Render
    screen.fill(pygame.Color('black'))
    if FULLSCREEN:
        # Scale preserving aspect ratio and center
        screen.blit(
            pygame.transform.scale(bitmap.surface,
                                   (SCALE_WIDTH, SCALE_HEIGHT)),
            ((WIDTH - SCALE_WIDTH) / 2, 0)
        )
    else:
        screen.blit(bitmap.surface, bitmap_rect)

    if showpalette:
        # Palette
        bitmap.palette.surface.set_palette(bitmap.palette.colors)
        screen.blit(bitmap.palette.surface, (690, 35))

        # System stats
        fps = int(clock.get_fps())
        stats_str = (f"fps: {fps} "
                     f"cpu: {cpu_percent}% mem: {mem_percent}%")
        stats = font.render(stats_str, True, pygame.Color('white'),
                            pygame.Color('black'))
        stats_rect = stats.get_rect()
        screen.blit(stats, (screen_rect.width - stats_rect.width - 50, 5))

    pygame.display.flip()

    # Cap framerate
    clock.tick(FPS)

pygame.quit()
