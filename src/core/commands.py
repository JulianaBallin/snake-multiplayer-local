"""Comandos de jogador (independentes de input)."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlayerCommand:
    """Comando enviado por um jogador a cada frame."""

    direction: tuple[int, int] | None = None
