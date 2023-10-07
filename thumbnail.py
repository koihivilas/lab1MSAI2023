import pygame
from element import Element
from event_types import Event_type

class Thumbnail(Element):
    def __init__(self, state, size, margin_x, margin_y, possible_states):
        super().__init__(margin_x, margin_y, size, size)
        self.state = state
        self.possible_states = possible_states

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

    def event(self, event_type, **kwargs):
        if(event_type == Event_type.MOUSE_WHEEL):
            self.change_state(kwargs['y'])

    def get_state(self):
        return self.state

    def change_state_forward(self):
        self.state = self.possible_states[(self.possible_states.index(self.state) + 1) % len(self.possible_states)]
    
    def change_state_backward(self):
        self.state = self.possible_states[(self.possible_states.index(self.state) - 1) % len(self.possible_states)]

    def change_state(self, mouse_wheel_direction):
        if mouse_wheel_direction > 0:
            self.change_state_backward()
        else:
            self.change_state_forward()