import random
from enum import Enum
from pygame.sprite import collide_circle
from AppConfig import AppConfig
import math
from Actor import ActorType

class WalkingActor:

    def __init__(self, col, row, colour, cfg: AppConfig, actorType=ActorType.BEING):
        self.previous_row = None
        self.previous_col = None
        
        self.actorType = actorType
        self.dir = random.randint(1, 4)

        r = random.randint(128, 255)
        g = random.randint(128, 255)        
        b = random.randint(128, 255)

        self.colour = colour
        self.colour = (r, g, b)
        
        self.col = col
        self.row = row
        self.cfg = cfg
        self.state_changed = True
        self.speed = 6
        self.angle = random.randint(0, 359)

        if self.angle == 0 or self.angle == 90 or self.angle == 270:
            self.angle += random.randint(1,3)
        
        if self.angle == 360:
            self.angle -+ random.randint(1,3)

        self.angle = float(math.radians(self.angle))
        a=2


    def get_small_change(self, max):

        mode = random.randint(0, 1)
        value = random.uniform(0, 1)
        value = value * max

        if mode:
            return value
        else:
            return value - 2 * value


    def update(self):
        if not self.actorType == ActorType.WALL:
            self.previous_col = self.col
            self.previous_row = self.row

            dx = self.speed * math.cos(self.angle)
            dy = self.speed * math.sin(self.angle)

            self.col = int(self.col + dx)
            self.row = int(self.row + dy)

            if self.col >= (self.cfg.col_count - 1) or self.col <= 0:
                self.angle = math.pi - self.angle + self.get_small_change(0.2)
    
            if self.row >= (self.cfg.row_count - 1) or self.row <= 0:
                self.angle = -self.angle + self.get_small_change(0.2)

            self.state_changed = True

            if self.previous_col == self.col:
                if self.previous_row == self.row:
                    self.state_changed = False

