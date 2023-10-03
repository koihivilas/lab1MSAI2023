import pygame
from settings import Settings as st

# TODO: use states instead of colors
class Node:
    def __init__(self, row, col, size, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.color = st.white
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows
        self.total_cols = total_cols

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

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row > 0 and not grid[self.row - 1][self.col].has_state(st.exit): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].has_state(st.exit): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].has_state(st.exit): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].has_state(st.exit): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False