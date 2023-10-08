from settings import Settings as st
import pygame
from element import Element

class Window(Element):
    def __init__(self, window, width, height) -> None:
        super().__init__(0, 0, width, height)
        self.__window = window
        self.__drawable_elments = {}
    
    @Element.element_draw_wraper
    def draw(self, window = None):
        if(window == None):
            window = self.__window
        for _, elements_by_priority in self.__drawable_elments.items():
            for element in elements_by_priority:
                element.draw(window)

    @Element.element_event_wraper
    def event(self, event_type, **kwargs):
        pos_x, pos_y = pygame.mouse.get_pos()
        reverse_priority_drawable_elments_list = sorted(self.__drawable_elments.items(), reverse = True)
        for _, elements_by_priority in reverse_priority_drawable_elments_list:
            for element in elements_by_priority:
                if element.is_coordinates_in_boundaries(pos_x, pos_y):
                    element.event(event_type, **kwargs)
    
    def add_element(self, element : Element, drawing_priority = 0):
        if(not self.enabled):
            return
        if(not drawing_priority in self.__drawable_elments.keys()):
            self.__drawable_elments[drawing_priority] = []
        self.__drawable_elments[drawing_priority].append(element)
        #make dictionary sorted by keys(priorities)
        self.__drawable_elments = dict(sorted(self.__drawable_elments.items()))