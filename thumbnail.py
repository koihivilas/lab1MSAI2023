import pygame
from element import Element
from event_types import Event_type
from event_args import Wheel_event_agrs
from event_handler import Event_handler
class Thumbnail(Element):
    def __init__(self, name, state, size, margin_x, margin_y, possible_states):
        super().__init__(name, margin_x, margin_y, size, size)
        self.state = state
        self.possible_states = possible_states
        Event_handler().add_handler(Event_type.ON_MOUSE_WHEEL,
                                    lambda args: self.mouse_wheel_handler(args))


    def get_x(self):
        pos_x, _ = pygame.mouse.get_pos()
        return pos_x + super().get_x()
    
    def get_y(self):
        _, pos_y = pygame.mouse.get_pos()
        return pos_y + super().get_y()
    
    @Element.element_draw_wraper
    def draw(self, window):
        color = self.state.value
        pygame.draw.rect(window, color, (self.get_x(), self.get_y(), self.get_width(), self.get_height()))
    
    @Element.element_handler_wraper
    def mouse_wheel_handler(self, args : Wheel_event_agrs):
        self.change_state(args.y)

    def get_state(self):
        return self.state
    
    def is_active(self):
        return self.enable and self.active

    def change_state_forward(self):
        self.state = self.possible_states[(self.possible_states.index(self.state) + 1) % len(self.possible_states)]
    
    def change_state_backward(self):
        self.state = self.possible_states[(self.possible_states.index(self.state) - 1) % len(self.possible_states)]

    def change_state(self, mouse_wheel_direction):
        if mouse_wheel_direction > 0:
            self.change_state_backward()
        else:
            self.change_state_forward()