from node import Node
from map_field_states import Map_field_state
from position import Position, Direction, CardinalDirections
from typing import List
class Map:
    def __init__(self, rows_amount, colums_amount) -> None:
        self.__width = colums_amount
        self.__height = rows_amount
        self.__table = [[
                        Node(i, j, default_state = Map_field_state.EMPTY) 
                         for j in range(self.__width)] 
                         for i in range(self.__height)]
        self.__trasures_positions = []
        self.__start_position = None
        self.__exits_positions = []
    #TODO: Remove
    def update_nodes_neighbors(self):
        table = self.__table
        for i in range(self.__height):
            for j in range(self.__width):
                node = table[i][j]
                node.neighbors = []

                if i > 0 and not table[i - 1][j].has_state(Map_field_state.EXIT): # UP
                    node.neighbors.append(table[i - 1][j])

                if j < self.__width - 1 and not table[i][j + 1].has_state(Map_field_state.EXIT): # RIGHT
                    node.neighbors.append(table[i][j + 1])

                if i < self.__height - 1 and not table[i + 1][j].has_state(Map_field_state.EXIT): # DOWN
                    node.neighbors.append(table[i + 1][j])

                if j > 0 and not table[i][j - 1].has_state(Map_field_state.EXIT): # LEFT
                    node.neighbors.append(table[i][j - 1])
    
    def get_posible_actions(self, position : Position) -> List[Direction]:
        table = self.__table
        x, y = position.x, position.y
        posible_moves = []
        if y > 0 and not table[y - 1][x].has_state(Map_field_state.EXIT):
            posible_moves.append(CardinalDirections.UP.value)

        if x < self.__width - 1 and not table[y][x + 1].has_state(Map_field_state.EXIT):
            posible_moves.append(CardinalDirections.RIGHT.value)

        if y < self.__height - 1 and not table[y + 1][x].has_state(Map_field_state.EXIT):
            posible_moves.append(CardinalDirections.DOWN.value)

        if x > 0 and not table[y][x - 1].has_state(Map_field_state.EXIT):
            posible_moves.append(CardinalDirections.LEFT.value)
        
        return posible_moves

    def is_treasure_position(self, position : Position):
        return self.__table[position.y][position.x].get_state() == Map_field_state.TREASURE
    
    def get_treasure_positions(self):
        return self.__trasures_positions

    def set_node_state(self, node_row, node_column, new_state):
        node = self.__table[node_row][node_column]
        if new_state == Map_field_state.START and self.__start_position:
            return
        if node.get_pos() not in self.__trasures_positions and node.get_pos() not in self.__exits_positions:
            node.set_state(new_state)
            if new_state == Map_field_state.TREASURE:
                self.__trasures_positions.append(Position(node_column, node_row))
            if new_state == Map_field_state.EXIT:
                self.__exits_positions.append(Position(node_column, node_row))
            if new_state == Map_field_state.START:
                self.__start_position = Position(node_column, node_row)

    def reset_node_state(self, node_row, node_column):
        node = self.__table[node_row][node_column]
        node.reset()
        position = node.get_pos()
        if(position in self.__trasures_positions):
            self.__trasures_positions.remove(position)
        if(position in self.__exits_positions):
            self.__exits_positions.remove(position)
        if(position == self.__start_position):
            self.__start_position = None
        
    def change_nodes_states(self, nodes_positions : List[Position], new_state):
        for position in nodes_positions:
            self.__table[position.y][position.x].set_state(new_state)
    
    def change_node_state(self, node_position, new_state):
        self.change_nodes_states([node_position], new_state)

    def get_start(self):
        return self.__start_position
    # DO NOT USE THIS FOR DIRECT ACESS TO NODES, ONLY FOR TABLE CLASS 
    def get_table(self):
        return self.__table
    
    def reset(self):
        for i in range(self.__height):
            for j in range(self.__width):
                self.__table[i][j].reset()

        for position in self.__trasures_positions:
            i,j = position.y, position.x
            self.__table[i][j].set_state(Map_field_state.TREASURE)
        for position in self.__exits_positions:
            i,j = position.y, position.x
            self.__table[i][j].set_state(Map_field_state.EXIT)
        if not self.__start_position is None:
            i, j = self.__start_position.y, self.__start_position.x
            self.__table[i][j].set_state(Map_field_state.START)
           
    def clear(self):
        for i in range(self.__height):
            for j in range(self.__width):
                self.__table[i][j].reset()
        self.__trasures_positions = []
        self.__start_position = None
        self.__exits_positions = []