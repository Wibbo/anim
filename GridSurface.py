import pygame
import numpy as np
from scipy import signal
from AppConfig import AppConfig
from typing import List
from WalkingActor import WalkingActor
from Actor import ActorType


class GridSurface:

    def __init__(self, cfg: AppConfig):
        """
        Constructor for the GridSurface class. Receives configuration settings.
        :param cfg: Configuration details from the INI file, adjusted and exposed as necessary by AppConfig.
        """
        self.cfg = cfg
        self.screen_width = cfg.screen_width_from_ini
        self.screen_height = cfg.screen_height_from_ini

        self.row_count = cfg.row_count
        self.col_count = cfg.col_count

        self.grid_colour = cfg.grid_colour
        self.inactive_cell_colour = cfg.inactive_cell_colour

        self.cell_width = self.screen_width // self.col_count
        self.screen_width = self.cell_width * self.col_count

        self.cell_height = self.screen_height // self.row_count
        self.screen_height = self.cell_height * self.row_count

        self.grid_thickness = cfg.grid_thickness

        pass

    def draw_actor(self, act, screen):
        if act.state_changed:
            if not act.actorType == ActorType.WALL:
                self.set_cell(screen, act.previous_col, act.previous_row, self.cfg.inactive_cell_colour)          
                self.set_cell(screen, act.col, act.row, act.colour)
      

    def draw_wall(self, act, screen):
        if act.actorType == ActorType.WALL:
            self.set_cell(screen, act.col, act.row, (128, 0, 0)) #TODO change this literal colour.       


    def update_walls(self, screen, walls: WalkingActor):
        for wall in walls:
            self.draw_wall(wall, screen)


    def update_actors(self, screen, actors: WalkingActor):
        for actor in actors:
            actor.straight_line_walk()
        for actor in actors:           
            self.draw_actor(actor, screen)


    def update_actor(self, screen, actor: WalkingActor):
            actor.straight_line_walk()     
            self.draw_actor(actor, screen)


    def draw_grid(self, screen):
        """
        Draws a rectangular grid on the supplied screen surface. Takes parameters from the ini file. The
        actual dimensions of the drawing surface are adjusted by AppConfig to fit the grid perfectly
        within the drawing surface.
        :param screen: A reference to the surface of the application window.
        :return: Nothing
        """
        if self.cfg.draw_grid:
            for row in range(self.row_count - 1):
                pygame.draw.line(screen, self.grid_colour, (0, (row + 1) * self.cell_height),
                    (self.screen_width, (row + 1) * self.cell_height), self.grid_thickness)
            
            for col in range(self.col_count - 1):
                pygame.draw.line(screen, self.grid_colour, ((col + 1) * self.cell_width, 0),
                    ((col + 1) * self.cell_width, self.screen_height), self.grid_thickness)
        
            pygame.draw.rect(screen, self.grid_colour, pygame.Rect(0, 0, self.screen_width + 1, self.screen_height + 1), self.grid_thickness)


    def get_cell_from_coordinate(self, pos):
        col = int(pos[0]/self.cell_width)  # Cell count across from zero.
        row = int(pos[1]/self.cell_height)  # Cell count down from zero.
        print(col, row)
        return row, col


    def is_cell_set():
        pass



    def set_cell(self, screen, col, row, rgb=(160, 0, 0)):
        """
        Draws a rectangle at the specified row and column position of the application's window grid.
        :param screen: A reference to the surface of the application window.
        :param row: The row at which to position the rectangle (starts at 0).
        :param col: The column at which to position the rectangle. (starts at 0).
        :param rgb: The rbg value for the colour of the rectangle being drawn.
        :return: Nothing.
        """
        left = col * self.cell_width + 1
        top = row * self.cell_height + 1
        width = self.cell_width - 1
        height = self.cell_height - 1

        pygame.draw.rect(screen, rgb, pygame.Rect(left, top, width, height))

  
    def clear_cell(self, screen, col, row):
        self.set_cell(self, screen, col, row, self.inactive_cell_colour)


