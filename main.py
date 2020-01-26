"""
An application for exploring John Conway's game of life.
Created by Matthew Weaver, 2019.
Uses PyGame for graphics rendering.
December 2019.
"""
import sys
import pygame.freetype
from AppConfig import AppConfig
from GridSurface import GridSurface
import pygame.freetype as ft


def read_config_file(ini_file_name):
    """
    Read parameters from the application config file.
    :param ini_file_name: The name of the ini file to read.
    :return: An object that represents the configuration parameters.
    """
    try:  # Changed something.
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


def generate_random_display():
    """
    Generates randomly activated cells in the current display grid.
    :return:
    """
    grid_display.fill((0, 0, 0))

    if cfg.draw_grid:
        gd.draw_grid(grid_display)

    gd.create_random_grid()
    gd.draw_cells_from_array(grid_display, gd.cell_array)


def display_info_text_line(screen, info_text, text_line):
    """
    Displays specified text in the application info bar.
    :param screen: A reference to the surface of the application window.
    :param info_text: The text to be displayed.
    :param text_line: The position of the text (from top to bottom).
    :return: Nothing.
    """
    x_pos = cfg.grid_width + 12
    y_pos = 10 + text_line * 16

    font.render_to(screen, (x_pos, y_pos), info_text, (255, 255, 255), (0, 0, 0), size=12)


def display_info_text_summary():
    """
    Displays a set of information in the application info bar.
    :return: Nothing.
    """
    display_info_text_line(grid_display, 'GENERAL INFO', 4)
    display_info_text_line(grid_display, f'App is running: {gol_is_running}  ', 5)
    display_info_text_line(grid_display, f'Current generation: {current_generation}     ', 6)
    display_info_text_line(grid_display, f'Timer ticks (1..60): {cfg.clock_ticks}     ', 7)

    display_info_text_line(grid_display, f'Total cell count: {cfg.column_count * cfg.row_count}   ', 9)
    display_info_text_line(grid_display, f'Live cell count: {gd.get_active_cell_count()}  ', 10)
    display_info_text_line(grid_display, f'Dead cell count: {gd.get_inactive_cell_count()}  ', 11)

    display_info_text_line(grid_display, f'KEY BINDINGS', 16)
    display_info_text_line(grid_display, 'R: Randomise the grid', 17)
    display_info_text_line(grid_display, 'G: Start grid updates', 18)
    display_info_text_line(grid_display, 'P: Pause grid updates', 19)
    display_info_text_line(grid_display, 'C: Clear the grid (pause if running)', 20)


def toggle_grid_cell(screen, mouse_position):
    """
    Toggles the state of the grid cell that was clicked.
        :param screen: A reference to the surface of the application window.
    :param mouse_position: The position of the mouse cursor when the mouse was clicked.
    :return: Nothing.
    """
    try:
        cell_row, cell_col = gd.get_cell_from_coordinate(mouse_position)

        if gd.is_cell_active(screen, cell_row, cell_col):
            gd.draw_inactive_cell(screen, cell_col, cell_row)
        else:
            gd.draw_active_cell(screen, cell_col, cell_row)
    except ValueError:
        pass


done = False
app_running = False

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

font = ft.Font('fonts/arial.ttf')


# ======================================================================================
# The main (infinite until interrupted) application loop.
# ======================================================================================
while not done:

    # Handle application interrupts - effectively mouse and keyboard input.
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggles the active state of the cell that is clicked.
            toggle_grid_cell(grid_display, event.pos)
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(event.key).upper()

            # React to specified keys.
            if key_pressed == 'R':
                generate_random_display()
                current_generation = 0
            if key_pressed == 'C':
                gol_is_running = False
                gd.clear_grid(grid_display)
            if key_pressed == 'G':
                gol_is_running = True
                gd.cell_array = gd.get_array_from_cells(grid_display)
            if key_pressed == 'P':
                gol_is_running = False

    if gol_is_running:
        gd.update_cell_array(grid_display)
        current_generation += 1

    display_info_text_summary()
    pygame.display.update()

    clock.tick(cfg.clock_ticks)
