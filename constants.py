from engine import colours, vec
from engine.io import keyboard


BACKGROUND_COLOUR        = colours.WHITE
BALL_COLOUR              = colours.RED
BAT_COLOUR               = colours.BLUE
NET_COLOR                = colours.BLACK
SCORE_COLOUR             = colours.GREEN
WIN_MESSAGE_COLOUR       = colours.YELLOW

FPS                      = 50
TPS                      = 50
ADC_SAMPLE_SIZE          = 10
PI_CONTROLLER_GPIO_PIN_1 = 9

WINNING_SCORE            = 10
SPIN_STRENGTH            = 0.4
SPIN_CURVE               = 2
BALL_N                   = 1
BALL_SPEED               = 50 # pixels / second
GAME_WIDTH               = 80
GAME_HEIGHT              = 24
BAT_SIZE                 = 3
SUPER_SIZE_BAT_SIZE      = 6
SUPER_SIZE_LENGTH        = 15
MAX_SUPER_SIZE_COUNT     = 2
RANDOM_SPEEDS            = True

USE_5_SERVE              = True
USE_ADAPTING_AVERAGE     = True
ADAPTING_AVERAGE_DECAY   = 0.9

if False: # set to True to use remote terminal with RaspberryPi
    from engine.io import remote_terminal
    ANSIISCREEN_OUTPUT      = remote_terminal.get_output()
else:
    ANSIISCREEN_OUTPUT      = lambda x: print(x, end="")
