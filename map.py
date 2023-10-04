from node import Node
from map_field_states import Map_field_state

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
    
    def set_node_state(self, node_row, node_column, new_state):
        node = self.__table[node_row][node_column]
        if new_state == Map_field_state.START and self.__start_position:
            return
        if node not in self.__trasures_positions:
            node.set_state(new_state)
            if new_state == Map_field_state.TREASURE:
                self.__trasures_positions.append((node_row, node_column))
            if new_state == Map_field_state.EXIT:
                self.__exits_positions.append((node_row, node_column))
            if new_state == Map_field_state.START:
                self.__start_position = (node_row, node_column)

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
        

    # DO NOT USE THIS FOR DIRECT ACESS TO NODES, ONLY FOR TABLE CLASS 
    def get_table(self):
        return self.__table
    
    def reset(self):
        for i in range(self.__height):
            for j in range(self.__width):
                self.__table[i][j].reset()

        for i,j in self.__trasures_positions:
            self.__table[i][j].set_state(Map_field_state.TREASURE)
        for i,j in self.__exits_positions:
            self.__table[i][j].set_state(Map_field_state.EXIT)
        if not self.__start_position is None:
            i, j = self.__start_position
            self.__table[i][j].set_state(Map_field_state.START)
           
    def clear(self):
        for i in range(self.__height):
            for j in range(self.__width):
                self.__table[i][j].reset()
        self.__trasures_positions = []
        self.__start_position = None
        self.__exits_positions = []