"""Gerenciamento de audio do jogo."""

from pathlib import Path

import pygame as pg


_ASSETS = Path(__file__).parent.parent.parent / "assets" / "sounds"

_MAPA_SONS: dict[str, str] = {
    "comida": "player_shoot.wav",
    "morte": "ship_explosion.wav",
    "sticky_orb": "asteroid_explosion.wav",
    "sticky_activated": "ufo_siren_small.wav",
}


class AudioManager:
    """Carrega e reproduz efeitos sonoros indexados por evento."""

    def __init__(self) -> None:
        pg.mixer.init()
        self._sons: dict[str, pg.mixer.Sound] = {}
        self._carregar()

    def _carregar(self) -> None:
        for evento, arquivo in _MAPA_SONS.items():
            caminho = _ASSETS / arquivo
            if caminho.exists():
                self._sons[evento] = pg.mixer.Sound(str(caminho))

    def tocar(self, evento: str) -> None:
        som = self._sons.get(evento)
        if som:
            som.play()
