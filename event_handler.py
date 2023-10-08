from event_types import Event_type
import pygame
from singleton import SingletonMeta
from event_args import *
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

class Event_handler(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.events = {event_type.name : Event() for event_type in Event_type}
    
    def add_handler(self, event_type : Event_type, handler):
        self.events[event_type.name].add_handler(handler)
    
    def remove_handler(self, event_type : Event_type, handler):
        self.events[event_type.name].remove_handler(handler)
    
    def reset_event_handlers(self, event_type : Event_type):
        self.events[event_type.name].reset()

    def reset_all_events(self):
        self.events = {event_type.name : Event() for event_type in Event_type}

    def handle_pygame(self, event, context, **kwarg):
        if event.type == pygame.MOUSEWHEEL:
            self.events[Event_type.ON_MOUSE_WHEEL.name].invoke(Wheel_event_agrs(event.y))
        elif event.type == pygame.BUTTON_RIGHT:
            pos_x, pos_y = pygame.mouse.get_pos()
            self.events[Event_type.ON_BUTTON_RIGHT.name].invoke(Click_event_args(pos_x, pos_y))
        elif event.type == pygame.BUTTON_LEFT:
            pos_x, pos_y = pygame.mouse.get_pos()
            self.events[Event_type.ON_BUTTON_LEFT.name].invoke(Click_event_args(pos_x, pos_y))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.events[Event_type.ON_K_SPACE.name].invoke()
            elif event.key == pygame.K_c:
                self.events[Event_type.ON_KEY_C.name].invoke()
            elif event.key == pygame.K_r:
                self.events[Event_type.ON_KEY_R.name].invoke()
            elif event.key == pygame.K_s:
                self.events[Event_type.ON_KEY_S.name].invoke()
            elif event.key == pygame.K_l:
                self.events[Event_type.ON_KEY_L.name].invoke()
        if pygame.mouse.get_pressed()[0]: # left click
            pos_x, pos_y = pygame.mouse.get_pos()
            self.events[Event_type.ON_BUTTON_LEFT_PRESSED.name].invoke(Click_event_args(pos_x, pos_y))
        elif pygame.mouse.get_pressed()[2]: # right click
            pos_x, pos_y = pygame.mouse.get_pos()
            self.events[Event_type.ON_BUTTON_RIGHT_PRESSED.name].invoke(Click_event_args(pos_x, pos_y))  