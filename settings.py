import pygame

# size of the window (default) proportion is 3 : 5
HEIGHT = 600
WIDTH = 1000

LIGHT_BLUE = (175, 238, 238) # Color of the closed (visited) nodes (default)
CLOSED = LIGHT_BLUE

LIGHT_GREEN = (152, 251, 152) # Color of the open nodes (default)
OPEN = LIGHT_GREEN

GREY = (128, 128, 128) # Color of the exits (default)
EXIT = GREY

SMOOTH_GREEN = (0, 221, 0) # Color of the start node (default)
START = SMOOTH_GREEN

RED_ORANGE = (238, 68, 0) # Color of the treasure (default)
TREASURE = RED_ORANGE

YELLOW = (255, 255, 0) # Color of the path nodes (default)
PATH = YELLOW

WHITE = (255, 255, 255) # Color of the empty nodes (default)
EMPTY = WHITE
LIGHT_GREY = (195, 195, 195) # Color of the grid (default)

HAS_STEP_DELAY = False
STEP_DELAY = 0.5 # seconds (default)

SHOWS_CURRENT_PATH = False
HAS_PATH_DELAY = False
PATH_DELAY = 0.005 # seconds (default)

# amount of rows and cols in the grid (default) proportion is 3 : 5
ROWS = 30
COLS = 50

THUMBNAIL_SIZE = 10 # size of the thumbnail following mouse cursor (default)
THUMBNAIL_MARGIN_X = 14 # margin of the thumbnail from mouse cursor (default)
THUMBNAIL_MARGIN_Y = 8 # margin of the thumbnail from mouse cursor (default)

DEPTH_LIMIT = 4 # depth limit for DFS (default)

# Uninformed search algorithms
BFS = "BFS"
DFS = "DFS"
DFS_DEPTH_LIMITED = "DFS Depth Limited"
BI_DIRECTIONAL = "Bi-Directional"

# Informed search algorithms
GREEDY = "Greedy"
A_STAR = "A*"
A_STAR_ITERATIVE = "A* Iterative"
JPS = "JPS"

GUI_PADDING_X = 200 # padding of the GUI (default) (right of the screen?)
GUI_PADDING_Y = 200 # padding of the GUI (default) (bottom of the screen?)

class Settings:
    # Grid and GUI
    rows = ROWS
    cols = COLS

    gui_padding_x = GUI_PADDING_X
    gui_padding_y = GUI_PADDING_Y

    # Pygame
    width = WIDTH
    height = HEIGHT

    window = pygame.display.set_mode((width + gui_padding_x, height + gui_padding_y))
    caption = pygame.display.set_caption("Path Finding Visualization")

    # States (colors)
    closed = CLOSED
    open = OPEN
    exit = EXIT
    start = START
    treasure = TREASURE
    path = PATH
    empty = EMPTY

    # Colors
    white = WHITE
    gray = GREY
    light_grey = LIGHT_GREY
    light_blue = LIGHT_BLUE
    light_green = LIGHT_GREEN
    smooth_green = SMOOTH_GREEN
    red_orange = RED_ORANGE
    yellow = YELLOW

    # Delays
    has_step_delay = HAS_STEP_DELAY
    step_delay = STEP_DELAY
    shows_current_path = SHOWS_CURRENT_PATH
    has_path_delay = HAS_PATH_DELAY
    path_delay = PATH_DELAY

    # Drawing tool
    thumbnail_size = THUMBNAIL_SIZE
    thumbnail_margin_x = THUMBNAIL_MARGIN_X
    thumbnail_margin_y = THUMBNAIL_MARGIN_Y

    # For DFS
    depth_limit = DEPTH_LIMIT

    def get_node_size():
        return Settings.width // Settings.cols if (Settings.width > Settings.height) else Settings.height // Settings.rows