"""Loop do jogo e transicao de cenas.

- InputMapper converte eventos do teclado em PlayerCommand.
- World atualiza a simulacao e gera eventos para Game reagir.
- Game gerencia transicoes de cena e renderizacao.
"""

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
        self.screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
        pg.display.set_caption("Snake Multiplayer Local")
        self.clock = pg.time.Clock()
        self.running = True

        font = pg.font.SysFont(C.FONT_NAME, C.FONT_SIZE)
        big = pg.font.SysFont(C.FONT_NAME, C.FONT_SIZE_BIG)
        self.renderer = Renderer(self.screen, fonts={"font": font, "big": big})

        self.scene = SceneState.MENU
        self.world = World()
        self.input_mapper = InputMapper()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(C.FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()
        pg.quit()

    def _handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._quit()

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self._quit()

            if self.scene == SceneState.MENU:
                if event.type == pg.KEYDOWN:
                    self.scene = SceneState.PLAY
                continue

            if self.scene == SceneState.GAME_OVER:
                if event.type == pg.KEYDOWN:
                    self.world.reset()
                    self.scene = SceneState.PLAY
                continue

            if self.scene == SceneState.PLAY:
                self.input_mapper.handle_event(event)

    def _update(self, dt: float) -> None:
        if self.scene != SceneState.PLAY:
            return

        commands = self.input_mapper.build_commands()
        self.world.update(dt, commands)

        if self.world.game_over:
            self.scene = SceneState.GAME_OVER

    def _draw(self) -> None:
        self.renderer.clear()

        if self.scene == SceneState.MENU:
            self.renderer.draw_menu()
        elif self.scene == SceneState.GAME_OVER:
            self.renderer.draw_game_over(self.world)
        else:
            self.renderer.draw_world(self.world)
            self.renderer.draw_hud(self.world)

        pg.display.flip()

    def _quit(self) -> None:
        self.running = False
        pg.quit()
        sys.exit(0)
