# BassieRacing - Constants

# The config constants class
class Config:
    # App constants
    NAME = 'BassieRacing'
    VERSION = '1.1.1'
    GIT_REPO_URL = 'https://github.com/bplaat/bassieracing'

    # Window constants
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60

    # Game constants
    TILE_SPRITE_SIZE = 128
    PIXELS_PER_METER = 18
    EXPLOSION_ANIMATION_FRAME_COUNT = 5
    EXPLOSION_ANIMATION_FRAME_TIME = 0.1
    COUNTDOWN_CLOCK_TICKS = 1
    COUNTDOWN_CLOCK_TICK_TIME = 0.1
    FINISH_LAP_TIME_TIMEOUT = 1.5

    # Editor constants
    EDITOR_CAMERA_BORDER = 12
    EDITOR_TILE_SIZE = 32
    EDITOR_DEFAULT_BRUSH_INDEX = 3
    MAP_DEFAULT_SIZES_INDEX = 1
    MAP_SIZES = [ 24, 32, 48, 64 ]
    MAP_SIZE_LABELS = [ 'Small', 'Medium', 'Large', 'Giant' ]
    MAP_DEFAULT_LAPS_INDEX = 2
    MAP_LAPS = [ 1, 2, 3, 4, 5, 6, 7, 8 ]
    MAP_DEFAULT_CRASH_TIMEOUT_INDEX = 0
    MAP_CRASH_TIMEOUTS = [ 0, 0.5, 1, 1.5, 2, 5, 10 ]

# The colors constants class
class Color:
    BLACK = ( 0, 0, 0 )
    DARK = ( 25, 25, 25 )
    GRAY = ( 125, 125, 125 )
    GREEN = ( 0, 255, 0 )
    LIGHT_GRAY = ( 225, 225, 225 )
    ORANGE = ( 255, 128, 0 )
    TRANSPARENT = ( 0, 0, 0, 0 )
    WHITE = ( 255, 255, 255 )
    YELLOW = ( 255, 255, 0 )

# The text align constants class
class TextAlign:
    LEFT = 0
    CENTER = 1
    RIGHT = 2

# The game mode constants class
class GameMode:
    SINGLE_PLAYER = 0
    SPLIT_SCREEN = 1
    MULTIPLAYER = 2

# The vehicle id constants class
class VehicleId:
    LEFT = 0
    RIGHT = 1

# The vehicle colors constants class
class VehicleColor:
    BLUE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLACK = 4

# The direction constants class
class Direction:
    TOP_TO_BOTTOM = 0
    BOTTOM_TO_TOP = 1
    LEFT_TO_RIGHT = 2
    RIGHT_TO_LEFT = 3
