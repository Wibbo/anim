"""
An application for exploring John Conway's game of life.
Created by Matthew Weaver, 2019.
Uses PyGame for graphics rendering.
"""

import sys
import pygame
from configuration import AppConfig
from DrawPrimitives import DrawPrimitives
done = False
app_running = False

cfg = AppConfig('GoL.ini')
dp = DrawPrimitives(cfg)

pygame.init()
clock = pygame.time.Clock()

display_window = pygame.display.set_mode((cfg.adjusted_screen_width, cfg.adjusted_screen_height))

dp.draw_grid(display_window)

# The main (infinite until interrupted) application loop.
while not done:

    # Handle application interrupts - effectively mouse and keyboard input.
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(event.key).upper()

            if key_pressed == 'F1':
                app_running = not app_running
                print(f'App running state is {app_running}')
            if key_pressed == 'F2':
                app_running = False
            if key_pressed == 'F3':
                pass
            if key_pressed == 'F4':
                pass

    pygame.display.update()
