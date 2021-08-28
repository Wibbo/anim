"""
Reads details from the application configuration file and presents them appropriately as application parameters.
"""

import configparser
import json
import numpy as np


class AppConfig:

    @staticmethod
    def string_to_boolean(parameter_value, parameter_name='Invalid entry'):

        if parameter_value == 'True':
            return True
        elif parameter_value == 'False':
            return False
        else:
            err_msg = f'The value of {parameter_name} in the GoL ini file is {parameter_value}. '
            err_msg += f'It must be either True or False. The application cannot continue.'
            raise KeyError(err_msg)

    @staticmethod
    def validate_setting(value, min_val, max_val):
        if min_val > max_val:
            raise KeyError

        if value < min_val:
            value = min_val
        elif value > max_val:
            value = max_val

        return value

    @staticmethod
    def file_exists(file_name):
        f = None

        try:
            f = open(file_name)
        except Exception as e:
            raise e
        finally:
            if f is not None:
                f.close()

    def __init__(self, cfg_file):
        """
        Constructor for the AppConfig class.
        Reads parameters from the specified configuration file
        and presents them appropriately to the application.
        :param cfg_file: The name of the configuration file to read.
        """
        AppConfig.file_exists(cfg_file)

        cfg = configparser.ConfigParser()
        cfg.read(cfg_file)

        self.row_count = int(cfg['GRID']['number_of_rows'])
        self.row_count = AppConfig.validate_setting(self.row_count, 2, 400)

        self.col_count = int(cfg['GRID']['number_of_columns'])
        self.col_count = AppConfig.validate_setting(self.col_count, 2, 500)

        self.title = cfg['GRID']['title']

        self.screen_width_from_ini = int(cfg['GRID']['screen_width'])
        self.screen_width_from_ini = AppConfig.validate_setting(self.screen_width_from_ini, 200, 2400)

        self.screen_height_from_ini = int(cfg['GRID']['screen_height'])
        self.screen_height_from_ini = AppConfig.validate_setting(self.screen_height_from_ini, 200, 1024)

        self.grid_thickness = int(cfg['GRID']['grid_thickness'])
        self.grid_thickness = AppConfig.validate_setting(self.grid_thickness, 1, 3)       

        self.grid_colour = json.loads(cfg['COLOUR']['grid_lines'])
        self.active_cell_colour = json.loads(cfg['COLOUR']['active_cell_colour'])
        self.inactive_cell_colour = json.loads(cfg['COLOUR']['inactive_cell_colour'])

        self.draw_grid = cfg['GRID']['draw_grid']
        self.draw_grid = AppConfig.string_to_boolean(self.draw_grid, 'draw_grid')

        self.clock_ticks = int(cfg['TIMING']['ticks_per_second'])
        self.clock_ticks = AppConfig.validate_setting(self.clock_ticks, 1, 400)




