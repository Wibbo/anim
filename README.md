# Game of Life

## Description  
Python implementation of John Conway's game of life using PyGame as a UI engine.  

## Application files  
#### main.py  
This is the entry point for the application. The key goals of this file are:  
* Read configuration values from the GoL.ini file.  
* Run the application, draw the application grid and update the status text in the sidebar.  
* Reacts to application key presses as defined in the **Application keys** section of this readme.  
* Contains the main PyGame loop that repeats until the application is stopped.  

#### AppConfig.py
Creates an in-memory structure for the application configuration file.

#### GridSurface.py
Represents the application grid, provides primitive drawing capabilities and game of life logic.

#### GameRules.py
* Defines rule-sets that govern how cells reproduce.
* There is a function called rule_x for each set of rules that are defined.
* More rules can be introduced by creating a new rule_x function. 
* The current rule-set is defined in the application configuration file.
* The rule_selector function activates a rule-set based on the rule number that is supplied.

## Application keys  
* R = Generate random grid of live and dead cells.  
* C = Clear the grid & stop the grid from updating if it is currently running.  
* G = Start grid update.  
* P = Pause grid updates.  

While the grid is paused, you can click any cell in the grid to toggle its on/off status.

## ini file settings  
#### [GRID]  
number_of_columns = The number of cells in the x direction.  
number_of_rows = The number of cells in the y direction.  
screen_width = The width of the screen in pixels.  
screen_height = The height of the screen in pixels.  
line_width = The width of the grid lines in pixels (currently forced to 1).  
draw_grid = If set to True, a grid is drawn. If set to False, no grid is drawn.  
info_bar_width = The width, in pixels, of the info bar on the right hand side of the application.  
live_cell_percentage = When randomising the grid, this is the percentage of random cells to create. 

#### [COLOUR]  
grid_lines = RGB colour of the grid lines e.g. [64, 64, 64]  
active_cell_colour = RGB colour for active cells e.g. [250, 250, 250]  
inactive_cell_colour = RGB colour for inactive cells e.g. [0, 0, 0]  

#### [TIMING] 
ticks_per_second = The number of times the screen is updated each second.

#### [ACTIONS] 
* show_cell_counts = If True, cell colours change from a dim red to white according to how many times they are resurrected. If False, live cells are always set to the active_cell_colour. 
* cell_reproduction_rule = A number that represents the rule-set to be applied to cell reproduction. Rules are defined in GameRules.py.
