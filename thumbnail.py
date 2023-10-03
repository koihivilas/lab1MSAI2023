import pygame

# TODO: it should be singleton, but I don't know how to do it in python
class Thumbnail:
    def __init__(self, state, size, margin_x, margin_y, possible_states):
        self.state = state
        self.size = size
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.possible_states = possible_states
        
    def draw(self, window):
        pos_x, pos_y = pygame.mouse.get_pos()
        pygame.draw.rect(window, self.state, (pos_x + self.margin_x, pos_y + self.margin_y, self.size, self.size))

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