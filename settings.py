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
LIGHT_GREY = (195, 195, 195) # Color of the grid (default)

HAS_STEP_DELAY = False
STEP_DELAY = 0.05 # seconds (default)

SHOWS_CURRENT_PATH = True
HAS_PATH_DELAY = False
PATH_DELAY = 0.005 # seconds (default)

# amount of rows and cols in the grid (default) proportion is 3 : 5
ROWS = 15
COLS = 25

THUMBNAIL_SIZE = 10 # size of the thumbnail following mouse cursor (default)
THUMBNAIL_MARGIN_X = 14 # margin of the thumbnail from mouse cursor (default)
THUMBNAIL_MARGIN_Y = 8 # margin of the thumbnail from mouse cursor (default)

DEPTH_LIMIT = 10 # depth limit for DFS (default)

class Settings:
    # Grid and GUI
    rows = ROWS
    cols = COLS

    # Pygame
    width = WIDTH
    height = HEIGHT
    window = pygame.display.set_mode((width, height))
    caption = pygame.display.set_caption("Path Finding Visualization")

    # States (colors)
    closed = CLOSED
    open = OPEN
    exit = EXIT
    start = START
    treasure = TREASURE
    path = PATH

    # Colors
    white = WHITE
    light_grey = LIGHT_GREY

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