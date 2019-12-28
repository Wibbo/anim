import pygame
import numpy


class GridDisplay:

    def __init__(self, cfg):
        """
        Constructor for the GridDisplay class. Receives configuration settings.
        :param cfg: Configuration details from the INI file, adjusted and exposed as necessary by AppConfig.
        """
        self.cfg = cfg

    def draw_grid(self, screen):
        """
        Draws a rectangular grid on the supplied screen surface. Takes parameters from the ini file. The
        actual dimensions of the drawing surface are adjusted by AppConfig to fit the grid perfectly
        within the drawing surface.
        :param screen: A reference to the surface of the application window.
        :return: Nothing
        """
        if self.cfg.draw_grid:
            # Draw the grid columns in the available screen window.
            for column in range(0, self.cfg.adjusted_screen_width, self.cfg.cell_width):
                pygame.draw.line(screen, self.cfg.grid_colour, (column, 0),
                                 (column, self.cfg.adjusted_screen_height), self.cfg.line_width)

            # Draw the grid rows in the available screen window.
            for row in range(0, self.cfg.adjusted_screen_height, self.cfg.cell_height):
                pygame.draw.line(screen, self.cfg.grid_colour, (0, row),
                                 (self.cfg.adjusted_screen_width, row), self.cfg.line_width)

    def draw_cell(self, screen, col, row, rgb):
        """
        Draws a rectangle at the specified row and column position of the application's window grid.
        :param screen: A reference to the surface of the application window.
        :param row: The row at which to position the rectangle (starts at 0).
        :param col: The column at which to position the rectangle. (starts at 0).
        :param rgb: The rbg value for the colour of the rectangle being drawn.
        :return: Nothing.
        """
        left = col * self.cfg.cell_width + self.cfg.line_width
        top = row * self.cfg.cell_height + self.cfg.line_width
        width = self.cfg.cell_width - 1
        height = self.cfg.cell_height - 1

        pygame.draw.rect(screen, rgb, pygame.Rect(left, top, width, height))

    def is_cell_active(self):
        pass


    def draw_active_cell(self, screen, col, row):
        """
        Draws a cell using the active cell colour defined in the INI file.
        :param screen: A reference to the surface of the application window.
        :param row: The row at which to position the rectangle (starts at 0).
        :param col: The column at which to position the rectangle. (starts at 0).
        :return: Nothing
        """
        self.draw_cell(screen, col, row, self.cfg.active_cell_colour)

    def draw_inactive_cell(self, screen, col, row):
        """
        Draws a cell using the inactive cell colour defined in the INI file.
        :param screen: A reference to the surface of the application window.
        :param row: The row at which to position the rectangle (starts at 0).
        :param col: The column at which to position the rectangle. (starts at 0).
        :return: Nothing
        """
        self.draw_cell(screen, col, row, self.cfg.inactive_cell_colour)






    def draw_cells_from_array(self, screen, grid_array):

        number_of_rows = grid_array.shape[0]
        number_of_columns = grid_array.shape[1]

        if number_of_rows != self.cfg.row_count:
            raise ValueError('The array parameter must have the same number of rows as the row count.')

        if number_of_columns != self.cfg.column_count:
            raise ValueError('The array parameter must have the same number of columns as the column count.')

        for i in range(number_of_rows):
            for j in range(number_of_columns):
                if grid_array[i][j] == 1:
                    self.draw_active_cell(screen, j, i)
                elif grid_array[i][j] == 0:
                    self.draw_inactive_cell(screen, j, i)
                else:
                    raise ValueError(f'All array elements should be zero or 1.')






    def get_array_from_cells(self):
        pass












