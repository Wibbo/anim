from WalkingActor import WalkingActor
from Actor import ActorType
import sys
import pygame.freetype
from AppConfig import AppConfig
from GridSurface import GridSurface
import pygame.freetype as ft
import random


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


# Read application parameters and create a grid surface object.
cfg = read_config_file('GoL.ini')
gd = GridSurface(cfg)


def create_actors(actor_count, list):
    for _ in range (actor_count):
        act_col = random.randint(0, cfg.col_count - 1)
        act_row = random.randint(0, cfg.row_count - 1)
        actor = WalkingActor(act_col, act_row, (255, 0, 0), cfg)
        list.append(actor)


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


def create_wall(screen, mouse_position, walls):
    """
    Toggles the state of the grid cell that was clicked.
        :param screen: A reference to the surface of the application window.
    :param mouse_position: The position of the mouse cursor when the mouse was clicked.
    :return: Nothing.
    """
    try:
        cell_row, cell_col = gd.get_cell_from_coordinate(mouse_position)
        
        wall_exists = False

        for w in walls:
            if w.col == cell_col:
                if w.row == cell_row:
                    wall_exists = True
                    break

        if not wall_exists:
            wall = WalkingActor(cell_col, cell_row, (128, 0, 0), cfg, ActorType.WALL)
            wall_list.append(wall)
    except ValueError:
        pass


actor_list = []
wall_list = []
done = False
app_running = False

create_actors(10, actor_list)
pygame.init()


clock = pygame.time.Clock()
gol_is_running = False

win_screen = pygame.display.set_mode((gd.screen_width + 1, gd.screen_height + 1))
pygame.display.set_caption(cfg.title)


if cfg.draw_grid:
    gd.draw_grid(win_screen)

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
            create_wall(win_screen, event.pos, wall_list)
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(event.key).upper()
            # React to specified keys.
            if key_pressed == 'P':
                gol_is_running = not gol_is_running

    if gol_is_running:
        gd.update_actors(win_screen, actor_list)
        gd.update_walls(win_screen, wall_list)
        pass

    pygame.display.update()
    clock.tick(cfg.clock_ticks)