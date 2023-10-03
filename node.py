import pygame
from settings import Settings as st

# TODO: use states instead of colors
class Node:
    def __init__(self, row, col, x, y):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.color = st.white
        self.neighbors = []

    def has_state(self, queryColor):
        return self.color == queryColor
    
    def set_state(self, queryColor):
        self.color = queryColor
    
    def get_pos(self):
        return self.row, self.col
    
    def reset(self):
        self.color = st.white
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    def __lt__(self, other):
        return False