"""Constantes de configuracao do jogo Snake."""

CELL = 20
COLS = 40
ROWS = 30
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL
FPS = 60

TICK_INTERVAL = 0.12

START_LENGTH = 4
FOOD_VALUE = 10
GROW_AMOUNT = 3
FOOD_COUNT = 3

BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
FOOD_COLOR = (200, 60, 60)
GRID_COLOR = (20, 20, 20)

PLAYER_COLORS = {
    1: (0, 220, 220),
    2: (220, 220, 0),
}
PLAYER_HEAD_COLORS = {
    1: (0, 150, 150),
    2: (160, 160, 0),
}

FONT_SIZE = 22
FONT_SIZE_BIG = 64
FONT_NAME = "consolas"

P1_START = (5, ROWS // 2)
P1_DIR = (1, 0)

P2_START = (COLS - 6, ROWS // 2)
P2_DIR = (-1, 0)
