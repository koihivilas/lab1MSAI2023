from enum import Enum
from settings import Settings as st

class NoValue(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)

class Map_field_state(NoValue):
    CLOSED = st.closed
    OPEN = st.open
    EXIT = st.exit
    START = st.start
    TREASURE = st.treasure
    PATH = st.path
    EMPTY = st.empty