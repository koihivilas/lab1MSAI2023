import pygame
class Element:
    def __init__(self, x, y, width, height, cursor = None) -> None:
        self.set_x(x)
        self.set_y(y)
        self.set_height(height)
        self.set_width(width)
        self.enabled = True
        self.visible = True
        self.active = True
        self.__cursor = cursor
    
    def draw(self, window):
        pass

    def event(self, event_type, **kwargs):
        pass
    
    def __draw_coursor(self, window):
        if(self.is_cursor_visible() and 
            self.is_coordinates_in_boundaries(self.get_cursor().get_x(), self.get_cursor().get_y())):
            self.get_cursor().draw(window)
    
    def element_draw_wraper(draw):
        def inner_function(self, window = None):
            if(not self.enabled or not self.visible):
                return
            draw(self, window)
            self.__draw_coursor(window)
        return inner_function

    def element_handler_wraper(event):
        def inner_function(self, **kwargs):
            if(not self.is_active()):
                return
            event(self, **kwargs)
        return inner_function
    
    #Getters and setters
    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x
        
    def get_y(self):
        return self.__y

    def set_y(self, y):
        self.__y = y

    def get_height(self):
        return self.__height

    def set_height(self, height):
        self.__height = height
        
    def get_width(self):
        return self.__width

    def set_width(self, width):
        self.__width = width

    def enable(self):
        self.visible = True
        self.active = True
        self.enabled = True

    def disable(self):
        self.visible = False
        self.active = False
        self.enabled = False

    def enable_events(self):
        self.active = True

    def disable_events(self):
        self.active = False

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def get_cursor(self):
        return self.__cursor
    
    def set_cursor(self, cursor):
        self.__cursor = cursor
    
    def is_active(self):
        pos_x, pos_y = pygame.mouse.get_pos()
        return self.enabled and self.active and self.is_coordinates_in_boundaries(pos_x, pos_y)
    
    def is_cursor_active(self):
        return self.get_cursor() and self.get_cursor().enabled and self.get_cursor().active
        
    def is_cursor_visible(self):
        return self.get_cursor() and self.get_cursor().enabled and self.get_cursor().visible

    def is_coordinates_in_boundaries(self, x, y):
        return x < self.get_x() + self.get_width() and x > self.get_x() and y < self.get_y() + self.get_height() and y > self.get_y()