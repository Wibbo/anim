from abc import ABC, abstractmethod
from AppConfig import AppConfig
from enum import Enum

class ActorType(Enum):
    WALL = 1
    BEING = 2

class Actor():

    def __init__(self, col, row, cfg: AppConfig, colour=(255,255,255), actorType=ActorType.BEING):
        self.previous_row = None
        self.previous_col = None
        
        self.actorType = actorType

        self.colour = colour
        
        self.col = col
        self.row = row
        self.cfg = cfg
        self.state_changed = True
        
