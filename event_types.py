from enum import Enum, auto

class Event_type(Enum):
    ON_BUTTON_RIGHT = auto()
    ON_BUTTON_LEFT = auto()
    ON_MOUSE_WHEEL = auto()
    ON_BUTTON_RIGHT_PRESSED = auto()
    ON_BUTTON_LEFT_PRESSED = auto()
    ON_K_SPACE = auto()
    ON_KEY_C = auto()
    ON_KEY_R = auto()
    ON_KEY_S = auto()
    ON_KEY_L  = auto()
    BEFORE_DRAW = auto()
    AFTER_DRAW = auto()
    ON_APP_STATE_CHANGE = auto()