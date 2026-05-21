"""Mapeamento de teclas para comandos de jogador."""

import pygame as pg

from core.commands import PlayerCommand

# Mesma ordem de jogadores do Asteroids Multiplayer Local:
# J1=WASD, J2=Setas, J3=IJKL, J4=Numpad
KEYMAPS: dict[int, dict[int, tuple[int, int]]] = {
    1: {
        pg.K_w: (0, -1), pg.K_s: (0, 1),
        pg.K_a: (-1, 0), pg.K_d: (1, 0),
    },
    2: {
        pg.K_UP: (0, -1), pg.K_DOWN: (0, 1),
        pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0),
    },
    3: {
        pg.K_i: (0, -1), pg.K_k: (0, 1),
        pg.K_j: (-1, 0), pg.K_l: (1, 0),
    },
    4: {
        pg.K_KP8: (0, -1), pg.K_KP2: (0, 1),
        pg.K_KP4: (-1, 0), pg.K_KP6: (1, 0),
    },
}


class InputMapper:
    """Converte eventos de teclado em PlayerCommand por jogador."""

    def __init__(self) -> None:
        self._pendente: dict[int, tuple[int, int] | None] = {
            pid: None for pid in KEYMAPS
        }

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type != pg.KEYDOWN:
            return
        for pid, mapa in KEYMAPS.items():
            if event.key in mapa:
                self._pendente[pid] = mapa[event.key]

    def build_commands(self) -> dict[int, PlayerCommand]:
        cmds = {pid: PlayerCommand(direction=self._pendente[pid]) for pid in KEYMAPS}
        self._pendente = {pid: None for pid in KEYMAPS}
        return cmds
