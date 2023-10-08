from enum import Enum
import math
class Position:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, __value: object) -> bool:
        if __value == None:
            return False
        return self.x == __value.x and self.y == __value.y
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __hash__(self) -> int:
        return int(self.x * 1000000 + self.y).__hash__()
    
    def manhattan(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def euclid(self, other) -> float:
        return math.sqrt(((self.x - other.x) ** 2 + (self.y - other.y) ** 2))
class Direction:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class CardinalDirections(Enum):
    RIGHT = Direction(1,0)
    DOWN = Direction(0, 1)
    LEFT = Direction(-1,0)
    UP = Direction(0,-1)