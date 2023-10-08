from settings import Settings as st
from element import Element
import pygame

BLACK = (0, 0, 0)

class Text(Element):
    def __init__(self, name,  x, y, width, height, text):
        super().__init__(name, x, y, width, height)
        self.__text = text

        self.__fontname = "arial"
        self.__fontsize = 20
        self.__fontcolor = BLACK
        self.set_font()
        self.render()
    
    def set_font(self):
        self.__font = pygame.font.SysFont(self.__fontname, self.__fontsize)
    
    def render(self):
        self.__img = self.__font.render(self.__text, True, self.__fontcolor)
        self.__rect = self.__img.get_rect()
        self.__pos = (self.get_x(), self.get_y())
        self.__rect.topleft = self.__pos
    
    def draw(self, window):
        window.blit(self.__img, self.__rect)

    # Setters and getters
    def get_text(self):
        return self.__text

    def get_width(self):
        return self.__rect.width

    def get_height(self):
        return self.__rect.height

    def set_text(self, text):
        self.__text = text
        self.render()
    
    def set_fontname(self, fontname):
        self.__fontname = fontname
        self.set_font()
        self.render()
    
    def set_fontsize(self, fontsize):
        self.__fontsize = fontsize
        self.set_font()
        self.render()
    
    def set_fontcolor(self, fontcolor):
        self.__fontcolor = fontcolor
        self.render()
