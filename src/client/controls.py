"""Mapeamento de teclas para comandos de jogador."""

import pygame as pg

from core.commands import PlayerCommand


class InputMapper:
    """Converte eventos de teclado em PlayerCommand por jogador."""

    KEYMAPS: dict[int, dict[int, tuple[int, int]]] = {
        1: {
            pg.K_w: (0, -1),
            pg.K_s: (0, 1),
            pg.K_a: (-1, 0),
            pg.K_d: (1, 0),
        },
        2: {
            pg.K_UP: (0, -1),
            pg.K_DOWN: (0, 1),
            pg.K_LEFT: (-1, 0),
            pg.K_RIGHT: (1, 0),
        },
    }

    def __init__(self) -> None:
        self._pendente: dict[int, tuple[int, int] | None] = {1: None, 2: None}

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type != pg.KEYDOWN:
            return
        for pid, mapa in self.KEYMAPS.items():
            if event.key in mapa:
                self._pendente[pid] = mapa[event.key]

    def build_commands(self) -> dict[int, PlayerCommand]:
        cmds = {
            pid: PlayerCommand(direction=self._pendente[pid])
            for pid in (1, 2)
        }
        self._pendente = {1: None, 2: None}
        return cmds
