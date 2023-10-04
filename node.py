import pygame
from settings import Settings as st
from position import Position

# TODO: use states instead of colors
class Node:
    def __init__(self, row, col, default_state):
        self.x = col
        self.y = row
        self.__default_state = default_state
        self.state = default_state
        self.neighbors = []

    def has_state(self, state):
        return self.state == state
    
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
    #TODO: Rename to get position
    def get_pos(self):
        return Position(self.x, self.y)
    
    def reset(self):
        self.state = self.__default_state

    def get_color(self):
        return self.state

    def __lt__(self, other):
        return False