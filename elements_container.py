from singleton import SingletonMeta

#TODO: It's timed solution, I just can't think about better one
class Elements_container(metaclass=SingletonMeta):
    def __init__(self):
        self.elements = {}

    def add_element(self, name, value):
        if(name in self.elements.keys()):
            raise Exception("Can't have two objects with same name")
        self.elements[name] = value 
