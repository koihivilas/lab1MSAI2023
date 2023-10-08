from settings import Settings as st
import pygame
from element import Element

class Window(Element):
    def __init__(self, name, window, width, height) -> None:
        super().__init__(name, 0, 0, width, height)
        self.__window = window
        self.__drawable_elments = {}
    
    @Element.element_draw_wraper
    def draw(self, window = None):
        if(window == None):
            window = self.__window
        for _, elements_by_priority in self.__drawable_elments.items():
            for element in elements_by_priority:
                element.draw(window)
    
    def add_element(self, element : Element, drawing_priority = 0):
        if(not self.enabled):
            return
        if(not drawing_priority in self.__drawable_elments.keys()):
            self.__drawable_elments[drawing_priority] = []
        self.__drawable_elments[drawing_priority].append(element)
        #make dictionary sorted by keys(priorities)
        self.__drawable_elments = dict(sorted(self.__drawable_elments.items()))