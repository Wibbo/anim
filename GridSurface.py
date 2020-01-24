import pygame
import numpy as np
from scipy import signal


class GridSurface:

    def __init__(self, cfg):
        """
        Constructor for the GridSurface class. Receives configuration settings.
        :param cfg: Configuration details from the INI file, adjusted and exposed as necessary by AppConfig.
        """
        self.cfg = cfg
        self.neighbour_array = None
        self.cell_array = np.zeros([self.cfg.row_count, self.cfg.column_count], dtype=int)
        self.count_array = np.zeros([self.cfg.row_count, self.cfg.column_count], dtype=int)

    def get_colour_from_count(self, row, col):
        col = self.count_array[row][col]

        if col > 255:
            return [255, 255, 255]

        if col < 50:
            col = 50

        return [col, 0, 0]

    def draw_grid(self, screen):
        """
        Draws a rectangular grid on the supplied screen surface. Takes parameters from the ini file. The
        actual dimensions of the drawing surface are adjusted by AppConfig to fit the grid perfectly
        within the drawing surface.
        :param screen: A reference to the surface of the application window.
        :return: Nothing
        """
        if self.cfg.draw_grid:

            for col in range(0, self.cfg.column_count + 1):
                pygame.draw.line(screen, self.cfg.grid_colour, (col * self.cfg.cell_width, 0),
                                 (col * self.cfg.cell_width, self.cfg.grid_height), self.cfg.line_width)

            for row in range(0, self.cfg.row_count + 1):
                pygame.draw.line(screen, self.cfg.grid_colour, (0, row * self.cfg.cell_height),
                                 (self.cfg.grid_width, row * self.cfg.cell_height), self.cfg.line_width)

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

    def draw_custom_cell(self, screen, col, row):
        """
        Draws a cell using the active cell colour defined in the INI file.
        :param screen: A reference to the surface of the application window.
        :param row: The row at which to position the rectangle (starts at 0).
        :param col: The column at which to position the rectangle. (starts at 0).
        :return: Nothing
        """
        rgb = self.get_colour_from_count(row, col)
        self.draw_cell(screen, col, row, rgb)

    def draw_active_cell(self, screen, col, row):
        """
        Draws a cell using the active cell colour defined in the INI file.
        :param screen: A reference to the surface of the application window.
        :param row: The row at which to position the rectangle (starts at 0).
        :param col: The column at which to position the rectangle. (starts at 0).
        :return: Nothing
        """
        # self.draw_cell(screen, col, row, self.cfg.active_cell_colour)

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
        """
        Sets cells in the screen grid based on the 2D array that is supplied. The array must be the same
        size as the grid and each element must be zero or one. If zero, the associated cell is reset
        to inactive_cell_colour. If one, the cell is set with active_cell_colour.
        :param screen: A reference to the surface of the application window.
        :param grid_array: An array representing the state of each cell.
        :return: Nothing.
        """
        number_of_rows = grid_array.shape[0]
        number_of_columns = grid_array.shape[1]

        if number_of_rows != self.cfg.row_count:
            raise ValueError('The array parameter must have the same number of rows as the row count.')

        if number_of_columns != self.cfg.column_count:
            raise ValueError('The array parameter must have the same number of columns as the column count.')

        for i in range(number_of_rows):
            for j in range(number_of_columns):
                if grid_array[i][j] == 1:
                    if self.cfg.show_cell_counts:
                        self.draw_custom_cell(screen, j, i)
                    else:
                        self.draw_active_cell(screen, j, i)
                elif grid_array[i][j] == 0:
                    self.draw_inactive_cell(screen, j, i)
                else:
                    raise ValueError(f'All array elements should be zero or 1.')

    def create_random_grid(self):
        """
        Creates a 2 dimensional numpy array that represents the application grid. Used mainly for
        testing, must be the same size as the rows and cols defined in the INI file.
        Each element is set randomly to either zero or 1.
        :return: The [row, col] array filled with ones or zeros.
        """
        cell_size = (self.cfg.row_count, self.cfg.column_count)
        self.cell_array = np.random.randint(2, size=cell_size)
        self.count_array = np.copy(self.cell_array)

    def get_cell_from_coordinate(self, pos):
        """
        Gets the integer position of the cell from the supplied coordinates.
        :param pos: A tuple containing the coordinates of the screen position in pixels
        from top left hand corner of the drawing surface.
        :return: The column and row position of the cell (zero based).
        """
        col = int(pos[0]/self.cfg.cell_width)  # Cell count across from zero.
        row = int(pos[1]/self.cfg.cell_height)  # Cell count down from zero.

        return row, col

    def is_cell_active(self, screen, row, col):
        """
        Determines if the cell at col, row is active. Active is determined by the colour of the
        cell. Black is treated as inactive, any other colour is treated as active.
        :param screen: A reference to the surface of the application window.
        :param row: The row at which to position the rectangle (starts at 0).
        :param col: The column at which to position the rectangle. (starts at 0).
        :return: True if the cell is active, False otherwise.
        """
        if row > self.cfg.row_count - 1:
            raise ValueError(f'Row out of bounds {row}')

        if col > self.cfg.column_count - 1:
            raise ValueError(f'Column out of bounds {col}')

        xcoord = int((col+1)*self.cfg.cell_width - self.cfg.cell_width/2)
        ycoord = int((row+1)*self.cfg.cell_height - self.cfg.cell_height/2)

        rgb_colour = screen.get_at((xcoord, ycoord))

        # TODO remove or configure this testing pixel.
        # screen.set_at((xcoord, ycoord), (255, 0, 0))

        if rgb_colour[0] * rgb_colour[1] * rgb_colour[2] == 0:
            return False
        else:
            return True

    def clear_grid(self, screen):
        cell_array = self.get_empty_grid_array()
        self.draw_cells_from_array(screen, cell_array)

    def get_empty_grid_array(self):
        """
        Creates an empty grid array.
        :return: A 2D empty array that represents the grid.
        """
        return np.zeros([self.cfg.row_count, self.cfg.column_count], dtype=int)

    def get_array_from_cells(self, screen):
        """
        Creates a 2D array that represents the current grid.
        :param screen: A reference to the surface of the application window.
        :return: An array that represents the current grid state.
        """
        cell_array = np.zeros([self.cfg.row_count, self.cfg.column_count], dtype=int)

        for i in range(self.cfg.row_count):
            for j in range(self.cfg.column_count):
                if self.is_cell_active(screen, i, j):
                    cell_array[i][j] = 1

        return cell_array

    def load_grid_with_pattern(self, pattern, x_pos, y_pos):
        """
        Creates a 2D array that represents the current grid.
        :param pattern: A reference to a pattern array.
        :param x_pos: x coordinate for the top left pattern element.
        :param y_pos: y coordinate for the top left pattern element.
        :return: An array that represents the current grid state.
        """
        self.cell_array[y_pos:y_pos+pattern.shape[0], x_pos:x_pos+pattern.shape[1]] = pattern
        return self.cell_array

    def get_cell_neighbours_array(self, screen):
        """
        Gets an array of neighbours from the existing grid.
        :param screen: A reference to the surface of the application window.
        :return: A 2D array representing neighbouring cell counts.
        """
        self.neighbour_array = self.cell_array.copy()

        neighbour_mask = np.ones((3, 3), dtype=int)
        neighbour_mask[1, 1] = 0
        self.neighbour_array = signal.convolve2d(self.cell_array, neighbour_mask, mode="same", boundary='wrap')

        return self.neighbour_array

    def update_cell_array(self, screen):
        """
        Generates an array of neighbouring cells and uses
        this to determine what happens to the existing cells.
        :param screen: A reference to the surface of the application window.
        :return: Nothing.
        """
        self.neighbour_array = self.get_cell_neighbours_array(screen)

        # Loop through the entire grid and update each cell.
        for row in range(0, self.cfg.row_count):
            for col in range(0, self.cfg.column_count):
                if self.cell_array[row][col] == 1:
                    if self.neighbour_array[row][col] < 2:
                        self.cell_array[row][col] = 0
                    if self.neighbour_array[row][col] >= 4:
                        self.cell_array[row][col] = 0
                    if self.neighbour_array[row][col] == 3:
                        self.cell_array[row][col] = 1
                    if self.neighbour_array[row][col] == 2:
                        self.cell_array[row][col] = 1
                if self.cell_array[row][col] == 0:
                    if self.neighbour_array[row][col] == 3:
                        self.cell_array[row][col] = 1
                    if self.cfg.six_neighbour_resurrection:
                        if self.neighbour_array[row][col] == 6:
                            self.cell_array[row][col] = 1

                if self.cell_array[row][col] == 1:
                    self.count_array[row][col] += 1

        # Update the grid.
        self.draw_cells_from_array(screen, self.cell_array)

    def get_total_cell_count(self):
        """
        The total number of cells in the currently defined grid.
        :return: The total cell count (basically equal to grid width * grid height).
        """
        if self.cell_array is not None:
            return np.size(self.cell_array)
        else:
            return 0

    def get_active_cell_count(self):
        """
        The total number of active (living) cells in the currently defined grid
        (the number of cells in the grid that are live).
        :return:  The total number of active cells.
        """
        if self.cell_array is not None:
            return np.count_nonzero(self.cell_array)
        else:
            return 0

    def get_inactive_cell_count(self):
        """
        The total number of inactive (dead) cells in the currently defined grid
        (the number of cells in the grid that are not live).
        :return:  The total number of inactive cells.
        """
        if self.cell_array is not None:
            return self.get_total_cell_count() - np.count_nonzero(self.cell_array)
        else:
            return 0





