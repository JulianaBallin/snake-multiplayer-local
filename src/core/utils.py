"""Utilitarios do jogo Snake."""

from random import choice
from core import config as C


def celulas_livres(ocupadas: set[tuple[int, int]]) -> list[tuple[int, int]]:
    return [
        (c, r)
        for c in range(C.COLS)
        for r in range(C.ROWS)
        if (c, r) not in ocupadas
    ]


def celula_aleatoria_livre(
    ocupadas: set[tuple[int, int]],
) -> tuple[int, int] | None:
    livres = celulas_livres(ocupadas)
    return choice(livres) if livres else None
