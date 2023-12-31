from element import Element
import pygame

class Cell(Element):
    def __init__(self, name, x, y, size, parent, linked_node = None):
        super().__init__(name, x, y, size, size)
        self.__parent = parent
        #Very dumb idea,  Cell saves link on Node which it represents
        self.__node = linked_node
    
    def link(self, linked_node):
        self.__node = linked_node

    def get_color(self):
        return self.__node.get_color() 

    def get_pos(self):
        return self.__parent.get_node_position_by_coordinates(self.get_x() + self.get_width() / 2, self.get_y() + self.get_height() / 2)
    
    @Element.element_draw_wraper
    def draw(self, window):
        color = self.get_color().value
        pygame.draw.rect(window, color, (self.get_x(), self.get_y(), self.get_width(), self.get_height()))