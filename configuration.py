import sys
import configparser
import json

class AppConfig:

    def __init__(self, cfg_file):

        # Read program parameters from the application configuration file.
        cfg = configparser.ConfigParser()
        cfg.read(cfg_file)

        self.row_count = int(cfg['GRID']['number_of_rows'])
        self.column_count = int(cfg['GRID']['number_of_columns'])
        self.initial_screen_width = int(cfg['GRID']['screen_width'])
        self.initial_screen_height = int(cfg['GRID']['screen_height'])
        self.line_width = int(cfg['GRID']['line_width'])
        self.draw_grid = bool(cfg['GRID']['draw_grid'])

        self.grid_colour = cfg['COLOUR']['grid_lines']
        self.active_cell_colour = json.loads(cfg['COLOUR']['active_cell_colour'])
        self.inactive_cell_colour = json.loads(cfg['COLOUR']['inactive_cell_colour'])

        pass
