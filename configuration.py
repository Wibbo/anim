"""
Reads details from the application configuration file and presents them appropriately as application parameters.
TODO: The line width parameter is currently forced to 1 since there is currently no need to consider other widths.
TODO: Consider removing the option to set line width in INI file.
"""

import configparser
import json


# Arbitrary configuration constraints
# Minimum rows 2, maximum rows 200
# min cols 2, max cols 400
# min width 200, max width 2400
# min height 200, max height 1024


class AppConfig:

    @staticmethod
    def string_to_boolean(string_setting):
        """
        Takes a string value of True of False and converts it to the corresponding boolean value.
        :param string_setting: The string to be converted (must be either True or False).
        :return: A boolean value.
        """
        if string_setting == 'True':
            return True
        elif string_setting == 'False':
            return False
        else:
            raise KeyError('Key value must be True or False')

    @staticmethod
    def validate_setting(value, min_val, max_val):
        if value < min_val:
            value = min_val
        elif value > max_val:
            value = max_val

        return value

    def __init__(self, cfg_file):
        """
        Constructor for the AppConfig class.
        Reads parameters from the specified configuration file
        and presents them appropriately to the application.
        :param cfg_file: The name of the configuration file to read.
        """
        cfg = configparser.ConfigParser()
        cfg.read(cfg_file)

        self.row_count = int(cfg['GRID']['number_of_rows'])
        self.row_count = self.validate_setting(self.row_count, 2, 200)

        self.column_count = int(cfg['GRID']['number_of_columns'])
        self.column_count = self.validate_setting(self.column_count, 2, 200)

        self.initial_screen_width = int(cfg['GRID']['screen_width'])
        self.initial_screen_width = self.validate_setting(self.initial_screen_width, 200, 2400)

        self.initial_screen_height = int(cfg['GRID']['screen_height'])
        self.initial_screen_height = self.validate_setting(self.initial_screen_height, 200, 1024)

        self.line_width = int(cfg['GRID']['line_width'])
        self.line_width = 1  # TODO: Forced to 1, no current use cases require anything else.

        self.cell_width = int(self.initial_screen_width / self.column_count)
        self.cell_height = int(self.initial_screen_height / self.row_count)

        self.adjusted_screen_width = int(self.cell_width * self.column_count) + self.line_width
        self.adjusted_screen_height = int(self.cell_height * self.row_count) + self.line_width

        self.draw_grid = cfg['GRID']['draw_grid']
        self.draw_grid = self.string_to_boolean(self.draw_grid)

        self.grid_colour = json.loads(cfg['COLOUR']['grid_lines'])
        self.active_cell_colour = json.loads(cfg['COLOUR']['active_cell_colour'])
        self.inactive_cell_colour = json.loads(cfg['COLOUR']['inactive_cell_colour'])

        self.draw_random_cells = cfg['ACTIONS']['draw_random_cells']
        self.draw_random_cells = self.string_to_boolean(self.draw_random_cells)

