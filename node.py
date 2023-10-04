import pygame
from settings import Settings as st

# TODO: use states instead of colors
class Node:
    def __init__(self, row, col, default_state):
        self.row = row
        self.col = col
        self.__default_state = default_state
        self.state = default_state
        self.neighbors = []

    def has_state(self, state):
        return self.state == state
    
    def set_state(self, state):
        self.state = state

    def get_pos(self):
        return self.row, self.col
    
    def reset(self):
        self.state = self.__default_state

    def get_color(self):
        return self.state

    def __lt__(self, other):
        return False