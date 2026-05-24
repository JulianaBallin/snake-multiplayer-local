"""Entidades do jogo Snake."""

from collections import deque
from typing import Deque


PlayerId = int


class Snake:
    """Cobra controlada por um jogador."""

    def __init__(
        self,
        player_id: PlayerId,
        start: tuple[int, int],
        direction: tuple[int, int],
        length: int,
    ) -> None:
        self.player_id = player_id
        self.direction = direction
        self.alive = True
        self.grow = 0

        # Estado da mecânica Rastro Grudento.
        self.sticky_charges = 0
        self.sticky_active_timer = 0.0
        self.slow_tick_counter = 0

        col, row = start
        dx, dy = direction

        self.body: Deque[tuple[int, int]] = deque(
            (col - dx * i, row - dy * i) for i in range(length)
        )

    @property
    def head(self) -> tuple[int, int]:
        return self.body[0]

    def set_direction(self, direction: tuple[int, int]) -> None:
        dx, dy = direction
        cx, cy = self.direction

        if (dx, dy) != (-cx, -cy):
            self.direction = (dx, dy)

    def move(self) -> None:
        hx, hy = self.head
        dx, dy = self.direction

        self.body.appendleft((hx + dx, hy + dy))

        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()


class Food:
    """Comida que aparece no tabuleiro."""

    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos


class StickyGoo:
    """Gosma deixada pelo Rastro Grudento."""

    def __init__(
        self,
        pos: tuple[int, int],
        owner_id: PlayerId,
        lifetime: float,
    ) -> None:
        self.pos = pos
        self.owner_id = owner_id
        self.lifetime = lifetime