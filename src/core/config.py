"""Constantes de configuracao do jogo Snake."""

CELL = 27
COLS = 40
ROWS = 30
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL
FPS = 60

TICK_INTERVAL = 0.12

START_LENGTH = 4
FOOD_VALUE = 10
GROW_AMOUNT = 3
FOOD_COUNT = 4

BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
FOOD_COLOR = (200, 60, 60)
GRID_COLOR = (20, 20, 20)

PLAYER_COLORS = {
    1: (60, 120, 255),
    2: (220, 220, 0),
    3: (0, 220, 80),
    4: (220, 60, 60),
}
PLAYER_HEAD_COLORS = {
    1: (40, 80, 200),
    2: (160, 160, 0),
    3: (0, 160, 60),
    4: (160, 40, 40),
}

FONT_SIZE = 20
FONT_SIZE_BIG = 64
FONT_SIZE_SMALL = 14
FONT_NAME = "consolas"

JOY_BTNS_PAUSE = (9,)

# (posicao_inicial, direcao_inicial) por jogador
PLAYER_STARTS: dict[int, tuple[tuple[int, int], tuple[int, int]]] = {
    1: ((5, ROWS // 2), (1, 0)),                   # esquerda, vai para direita
    2: ((COLS - 6, ROWS // 2), (-1, 0)),            # direita, vai para esquerda
    3: ((COLS // 4, ROWS // 4), (0, 1)),            # canto superior esquerdo, vai para baixo
    4: ((3 * COLS // 4, 3 * ROWS // 4), (0, -1)),  # canto inferior direito, vai para cima
}

# Configuracoes do poder "Sticky Trail"
STICKY_ACTIVE_DURATION = 5.0
STICKY_GOO_DURATION = 10.0
STICKY_ATTRACTION_RADIUS = 4
STICKY_SLOW_CYCLE = 5
STICKY_SLOW_SKIPPED_TICKS = 2
STICKY_ORB_SPAWN_CHANCE = 0.2

STICKY_COLOR = (150, 60, 220)
STICKY_ORB_COLOR = (190, 80, 255)