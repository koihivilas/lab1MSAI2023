from enum import Enum, auto

class Event_type(Enum):
    BUTTON_RIGHT = auto()
    BUTTON_LEFT = auto()
    MOUSE_WHEEL = auto()
    KEY_PRESSED = auto()
    BUTTON_RIGHT_PRESSED = auto()
    BUTTON_LEFT_PRESSED = auto()