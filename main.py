"""
An application for exploring John Conway's game of life.
Created by Matthew Weaver, 2019.
Uses PyGame for graphics rendering.
"""

import sys
import pygame.freetype
from AppConfig import AppConfig
from GridSurface import GridSurface

done = False
app_running = False


def display_help():
    """
    Display help for the application.
    :return: Nothing.
    """
    print()
    print('APPLICATION OPTIONS')
    print('===================')
    print('Clicking on any cell toggles its active state.')

    print('A: Create an array from the current status of the grid cells and display it.')
    print('C: Clears the grid of all active cells (pauses the game if it is not already paused).')
    print('R: Create a random 2D array representing the grid and set cell statuses accordingly.')
    print('N: Create a neighbours array for the current grid and display it.')


def read_config_file(ini_file_name):
    """
    Read parameters from the application config file.
    :param ini_file_name: The name of the ini file to read.
    :return: An object that represents the configuration parameters.
    """
    try:
        params = AppConfig(ini_file_name)
    except FileNotFoundError as ff:
        print(ff)
        sys.exit()
    except KeyError as ke:
        print(f'Cannot find {ke} parameter in the ini file, The application cannot continue.')
        sys.exit()
    except ValueError as ve:
        print(ve)
        sys.exit()
    except Exception as e:  # noqa
        print(f'Unexpected error: has occurred, The application cannot continue.')
        sys.exit()
    else:
        return params


pygame.init()

# Read application parameters and create a grid surface object.
cfg = read_config_file('GoL.ini')
gd = GridSurface(cfg)

clock = pygame.time.Clock()
gol_is_running = False
current_generation = 0

grid_display = pygame.display.set_mode((cfg.window_width, cfg.window_height))

if cfg.draw_grid:
    gd.draw_grid(grid_display)

# The main (infinite until interrupted) application loop.
while not done:

    # Handle application interrupts - effectively mouse and keyboard input.
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggles the active state of the cell that is clicked.
            cell_row, cell_col = gd.get_cell_from_coordinate(event.pos)
            if gd.is_cell_active(grid_display, cell_row, cell_col):
                gd.draw_inactive_cell(grid_display, cell_col, cell_row)
            else:
                gd.draw_active_cell(grid_display, cell_col, cell_row)
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(event.key).upper()

            # React to specified keys.
            if key_pressed == 'H':
                display_help()
            if key_pressed == 'A':
                print('Creating an array from the cell grid (examining pixel colour')
                print(gd.get_array_from_cells(grid_display))
            if key_pressed == 'R':
                print('Drawing cells from a randomly generated array.')
                cell_array = gd.get_randomly_activated_cell_array()
                gd.draw_cells_from_array(grid_display, cell_array)
                print(cell_array)
            if key_pressed == 'N':
                print('Creating a cell neighbours array.')
                neigbour_array = gd.get_cell_neighbours_array(grid_display)
                print(neigbour_array)
            if key_pressed == 'C':
                gol_is_running = False
                gd.clear_grid(grid_display)
            if key_pressed == 'G':
                gol_is_running = True
                gd.cell_array = gd.get_array_from_cells(grid_display)
            if key_pressed == 'S':
                gol_is_running = False
            if key_pressed == 'I':
                print('APPLICATION STATUS')

    if gol_is_running:
        gd.update_cell_array(grid_display)
        current_generation += 1

    # TODO: Look at optimising this by passing a list of rectangles that have changed for certain actions.
    pygame.display.update()

    clock.tick(4)
