from event_types import Event_type
import pygame

class Event():
    def __init__(self) -> None:
        self.__handlers = []

    def add_handler(self, handler):
        self.__handlers.append(handler)

    def remove_handler(self, handler):
        self.__handlers.remove(handler)
    
    def reset(self):
        self.__handlers.clear()
    
    def invoke(self, *args):
        for handler in self.__handlers:
            handler(*args)

#Implementation from https://refactoring.guru/design-patterns/singleton/python/example#example-0
class SingletonMeta(type): 
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Event_handler(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.events = {event_type.name : Event() for event_type in Event_type}
    
    def add_handler(self, event_type : Event_type, handler):
        self.events[event_type].add_handler(handler)
    
    def remove_handler(self, event_type : Event_type, handler):
        self.events[event_type].remove_handler(handler)
    
    def reset_event_handlers(self, event_type : Event_type):
        self.events[event_type].reset()

    def reset_all_events(self):
        self.events = {event_type.name : Event() for event_type in Event_type}

    def handle_pygame(self, event, context, **kwarg):
        if event.type == pygame.MOUSEWHEEL:
            self.events[Event_type.ON_MOUSE_WHEEL].invoke(event_args)
        elif event.type == pygame.BUTTON_RIGHT:
            self.events[Event_type.ON_BUTTON_RIGHT].invoke(event_args)
        elif event.type == pygame.BUTTON_LEFT:
            self.events[Event_type.ON_BUTTON_LEFT].invoke(event_args)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.events[Event_type.ON_KEY_SPACE].invoke(event_args)
            elif event.key == pygame.K_c:
                self.events[Event_type.ON_KEY_C].invoke(event_args)
            elif event.key == pygame.K_r:
                self.events[Event_type.ON_KEY_R].invoke(event_args)
            elif event.key == pygame.K_s:
                self.events[Event_type.ON_KEY_S].invoke(event_args)
            elif event.key == pygame.K_l:
                self.events[Event_type.ON_KEY_L].invoke(event_args)
        if pygame.mouse.get_pressed()[0]: # left click
            self.events[Event_type.ON_BUTTON_LEFT_PRESSED].invoke(event_args)
        elif pygame.mouse.get_pressed()[2]: # right click
            self.events[Event_type.ON_BUTTON_RIGHT_PRESSED].invoke(event_args)  