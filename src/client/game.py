"""Loop principal do jogo e transicoes de cena."""

import sys

import pygame as pg

from core import config as C
from core.scene import SceneState
from core.world import World
from client.controls import InputMapper
from client.renderer import Renderer


class Game:
    """Orquestra input -> update -> draw."""

    def __init__(self) -> None:
        pg.init()

        self._tela = pg.display.set_mode((C.WIDTH, C.HEIGHT))
        self._relogio = pg.time.Clock()
        self._rodando = True

        pg.display.set_caption("Snake Multiplayer Local")

        fontes = {
            "normal": pg.font.SysFont(C.FONT_NAME, C.FONT_SIZE),
            "grande": pg.font.SysFont(C.FONT_NAME, C.FONT_SIZE_BIG),
            "pequena": pg.font.SysFont(C.FONT_NAME, C.FONT_SIZE_SMALL),
        }

        self._renderer = Renderer(self._tela, fontes)
        self._input = InputMapper()
        self._world = World()
        self._cena = SceneState.MENU

    def rodar(self) -> None:
        while self._rodando:
            dt = self._relogio.tick(C.FPS) / 1000.0
            self._processar_eventos()
            self._atualizar(dt)
            self._renderizar()
        pg.quit()

    def _processar_eventos(self) -> None:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                self._encerrar()

            if evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE:
                self._encerrar()

            if self._cena == SceneState.MENU:
                if evento.type == pg.KEYDOWN:
                    self._cena = SceneState.PLAY
                continue

            if self._cena == SceneState.GAME_OVER:
                if evento.type == pg.KEYDOWN:
                    self._world.reset()
                    self._cena = SceneState.PLAY
                continue

            self._input.processar_evento(evento)

    def _atualizar(self, dt: float) -> None:
        if self._cena != SceneState.PLAY:
            return

        comandos = self._input.gerar_comandos()
        self._world.update(dt, comandos)

        if self._world.game_over:
            self._cena = SceneState.GAME_OVER

    def _renderizar(self) -> None:
        self._renderer.limpar()

        if self._cena == SceneState.MENU:
            self._renderer.desenhar_menu(self._input.status_joysticks())
        elif self._cena == SceneState.GAME_OVER:
            self._renderer.desenhar_fim_de_jogo(self._world)
        else:
            self._renderer.desenhar_mundo(self._world)
            self._renderer.desenhar_hud(self._world)

        pg.display.flip()

    def _encerrar(self) -> None:
        self._rodando = False
        pg.quit()
        sys.exit(0)
