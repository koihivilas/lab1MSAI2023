class Element:
    def __init__(self, x, y, width, height, cursor = None) -> None:
        self.set_x(x)
        self.set_y(y)
        self.set_height(height)
        self.set_width(width)
        self.enabled = True
        self.__cursor = cursor
    
    def draw(self):
        pass

    def event(self, event_type, **kwargs):
        pass

    
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
        self.__enabled = True

    def disable(self):
        self.__enabled = False

    def get_cursor(self):
        return self.__cursor
    
    def set_cursor(self, cursor):
        self.__cursor = cursor
    
    def is_cursor_active(self):
        return self.get_cursor() and self.get_cursor().enabled
    
    def is_coordinates_in_boundaries(self, x, y):
        return x < self.get_x() + self.get_width() and x > self.get_x() and y < self.get_y() + self.get_height() and y > self.get_y()