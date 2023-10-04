from cell import Cell
from settings import Settings as st
from event_types import Event_type
from element import Element
from map import Map
import pygame
class Table(Element):
    def __init__(self, x, y, width, height, node_size, data_source : Map = None, cell_default_color = st.white, mouse_thumbnail = None) -> None:
        super().__init__(x, y, width, height, mouse_thumbnail)
        self.__node_size = node_size
        self.__data_source = data_source
        self.__table = [[
                        Cell(x + j * node_size, y + i * node_size, node_size, 
                             linked_node = self.__data_source.get_table()[i][j],
                             parent = self) 
                         for j in range(self.get_width() // node_size)] 
                         for i in range(self.get_height() // node_size)]
        if data_source is not None:
            self.link_table(self.__data_source)

    def draw(self, window):
        for i in range(self.get_height() // self.__node_size):
            for j in range(self.get_width() // self.__node_size):
                self.__table[i][j].draw(window)
        self.__draw_grid(window)
        if(self.is_cursor_active() and 
            self.is_coordinates_in_boundaries(self.get_cursor().get_x(), self.get_cursor().get_y())):
            self.get_cursor().draw(window)
    
    def event(self, event_type : Event_type, **kwargs):
        if(not self.enabled):
            return
        
        if(event_type == Event_type.BUTTON_LEFT_PRESSED):
            node_row, node_col = self.get_node_position_by_coordinates(x = kwargs['x'], y = kwargs['y'])
            #Closly tie coursor with thumbnail realization
            self.__data_source.set_node_state(node_row, 
                                                  node_col, 
                                                  new_state = self.get_cursor().get_state())
        if(event_type == Event_type.BUTTON_RIGHT_PRESSED):
            node_row, node_col = self.get_node_position_by_coordinates(x = kwargs['x'], y = kwargs['y'])
            #Closly tie coursor with thumbnail realization
            self.__data_source.reset_node_state(node_row, 
                                                  node_col) 
            
        if(self.is_cursor_active()):
            self.get_cursor().event(event_type, **kwargs)

    def link_table(self, data_source : Map):
        self.__data_source = data_source
        for i in range(self.get_height() // self.__node_size):
            for j in range(self.get_width() // self.__node_size):
                self.__table[i][j].link(self.__data_source.get_table()[i][j])

    def get_node_position_by_coordinates(self, x, y):
        row = y // self.__node_size
        col = x // self.__node_size
        return row, col
    
    def __draw_grid(self, window):
        for i in range(self.get_height() // self.__node_size + 1):
            line_start_vector = (self.get_x(), self.get_y() + i * self.__node_size)
            line_end_vector = (self.get_x() + self.get_width(), self.get_y()+ i * self.__node_size)
            pygame.draw.line(window, st.light_grey, line_start_vector, line_end_vector)
        
        for i in range(self.get_width() // self.__node_size):
            line_start_vector = (self.get_x() + i * self.__node_size, self.get_y())
            line_end_vector = (self.get_x() + i * self.__node_size, self.get_y() + self.get_height())
            pygame.draw.line(window, st.light_grey, line_start_vector, line_end_vector)

    
