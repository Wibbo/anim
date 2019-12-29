"""
An application for exploring John Conway's game of life.
Created by Matthew Weaver, 2019.
Uses PyGame for graphics rendering.
"""

import sys
import pygame
from AppConfig import AppConfig
from GridSurface import GridSurface

done = False
app_running = False


def display_help():
    """
    Display help for the application.
    :return: Nothing.
    """
    print('Clicking on any cell toggles its active state.')
    print('A: Create an array from the current status of the grid cells and display it.')
    print('R: Create a random 2D array representing the grid and set cell statuses accordingly.')
    print('N: Create a neighbours array for the current grid and display it.')

def read_config_file(ini_file_name):
    """
    Reads and validates parameters from the application ini file.
    :return: A parameters object.
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


# Read application parameters and create a grid surface object.
cfg = read_config_file('GoL.ini')
gd = GridSurface(cfg)

pygame.init()
clock = pygame.time.Clock()

start_game_of_life = False

display_window = pygame.display.set_mode((cfg.adjusted_screen_width, cfg.adjusted_screen_height))

if cfg.draw_grid:
    gd.draw_grid(display_window)

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
            if gd.is_cell_active(display_window, cell_row, cell_col):
                gd.draw_inactive_cell(display_window, cell_col, cell_row)
            else:
                gd.draw_active_cell(display_window, cell_col, cell_row)
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(event.key).upper()

            # React to specified keys.
            if key_pressed == 'H':
                display_help()
            if key_pressed == 'A':
                print('Creating an array from the cell grid (examining pixel colour')
                print(gd.get_array_from_cells(display_window))
            if key_pressed == 'R':
                print('Drawing cells from a randomly generated array.')
                cell_array = gd.get_randomly_activated_cell_array()
                gd.draw_cells_from_array(display_window, cell_array)
                print(cell_array)
            if key_pressed == 'N':
                print('Creating a cell neighbours array.')
                neigbour_array = gd.get_cell_neighbours_array(display_window)
                print(neigbour_array)
            if key_pressed == 'G':
                start_game_of_life = True
            if key_pressed == 'S':
                start_game_of_life = False
            if key_pressed == 'F4':
                pass

    if start_game_of_life:
        gd.update_cell_array(display_window)

    # TODO: Look at optimising this by passing a list of rectangles that have changed for certain actions.
    pygame.display.update()

    clock.tick(10)