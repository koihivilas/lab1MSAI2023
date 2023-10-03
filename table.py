from node import Node
from settings import Settings as st
import pygame

class Table:
    def __init__(self, x, y, rows_amount, columns_amount, node_size) -> None:
        self.__x = x
        self.__y = y
        self.__width = columns_amount
        self.__height = rows_amount
        self.__node_size = node_size
        self.__table = [[Node(i, j, x + j * node_size, y + i * node_size) for j in range(self.__width)] for i in range(self.__height)]
        self.reset_table()

    def reset_table(self):
        for i in range(self.__height):
            for j in range(self.__width):
                self.__table[i][j].reset()
    
    def update_nodes_neighbors(self):
        table = self.__table
        for i in range(self.__height):
            for j in range(self.__width):
                node = table[i][j]
                node.neighbors = []

                if i > 0 and not table[i - 1][j].has_state(st.exit): # UP
                    node.neighbors.append(table[i - 1][j])

                if j < self.__width - 1 and not table[i][j + 1].has_state(st.exit): # RIGHT
                    node.neighbors.append(table[i][j + 1])

                if i < self.__height - 1 and not table[i + 1][j].has_state(st.exit): # DOWN
                    node.neighbors.append(table[i + 1][j])

                if j > 0 and not table[i][j - 1].has_state(st.exit): # LEFT
                    node.neighbors.append(table[i][j - 1])

    def __draw_grid(self, window):
        for i in range(self.__height + 1):
            line_start_vector = (self.x, self.y + i * self.__node_size)
            line_end_vector = (self.x + self.__width * self.__node_size, self.y + i * self.__node_size)
            pygame.draw.line(window, st.light_grey, line_start_vector, line_end_vector)
        
        for i in range(self.__width):
            line_start_vector = (self.x + i * self.__node_size, self.y)
            line_end_vector = (self.x + i * self.__node_size, self.y + self.__height * self.__node_size)
            pygame.draw.line(window, st.light_grey, line_start_vector, line_end_vector)

    def draw(self, window):
        self.__draw_grid()
        for i in range(self.__height):
            for j in range(self.__width):
                self.__table[i][j].draw(window)
