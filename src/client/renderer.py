"""Renderizacao do jogo Snake usando pygame."""

import pygame as pg

from core import config as C
from core.entities import Food, Snake
from core.scene import SceneState


class Renderer:
    """Desenha cenas e entidades sem acoplar regras do jogo."""

    def __init__(
        self,
        screen: pg.Surface,
        fonts: dict[str, pg.font.Font],
    ) -> None:
        self.screen = screen
        self.font = fonts["font"]
        self.big = fonts["big"]

    def clear(self) -> None:
        self.screen.fill(C.BLACK)

    def draw_grid(self) -> None:
        for c in range(C.COLS + 1):
            x = c * C.CELL
            pg.draw.line(self.screen, C.GRID_COLOR, (x, 0), (x, C.HEIGHT))
        for r in range(C.ROWS + 1):
            y = r * C.CELL
            pg.draw.line(self.screen, C.GRID_COLOR, (0, y), (C.WIDTH, y))

    def draw_world(self, world: object) -> None:
        self.draw_grid()
        for food in world.foods:
            self._draw_food(food)
        for snake in world.snakes.values():
            if snake.alive:
                self._draw_snake(snake)

    def _draw_food(self, food: Food) -> None:
        col, row = food.pos
        rect = pg.Rect(
            col * C.CELL + 3,
            row * C.CELL + 3,
            C.CELL - 6,
            C.CELL - 6,
        )
        pg.draw.ellipse(self.screen, C.FOOD_COLOR, rect)

    def _draw_snake(self, snake: Snake) -> None:
        cor = C.PLAYER_COLORS[snake.player_id]
        cor_cabeca = C.PLAYER_HEAD_COLORS[snake.player_id]
        for i, (col, row) in enumerate(snake.body):
            rect = pg.Rect(
                col * C.CELL + 1,
                row * C.CELL + 1,
                C.CELL - 2,
                C.CELL - 2,
            )
            c = cor_cabeca if i == 0 else cor
            pg.draw.rect(self.screen, c, rect, border_radius=4)

    def draw_hud(self, world: object) -> None:
        p1_score = world.scores.get(1, 0)
        p2_score = world.scores.get(2, 0)
        p1_viva = world.snakes[1].alive if 1 in world.snakes else False
        p2_viva = world.snakes[2].alive if 2 in world.snakes else False

        p1_status = "VIVO" if p1_viva else "MORTO"
        p2_status = "VIVO" if p2_viva else "MORTO"

        label1 = self.font.render(
            f"J1 {p1_score:04d} [{p1_status}]",
            True,
            C.PLAYER_COLORS[1],
        )
        label2 = self.font.render(
            f"J2 {p2_score:04d} [{p2_status}]",
            True,
            C.PLAYER_COLORS[2],
        )
        self.screen.blit(label1, (10, 5))
        self.screen.blit(label2, (C.WIDTH - label2.get_width() - 10, 5))

    def draw_menu(self) -> None:
        title = self.big.render("SNAKE", True, C.WHITE)
        sub = self.font.render(
            "Pressione qualquer tecla para iniciar",
            True,
            C.WHITE,
        )
        ctrl = self.font.render(
            "J1: WASD     J2: Setas direcionais",
            True,
            C.PLAYER_COLORS[1],
        )
        cx = C.WIDTH // 2
        self.screen.blit(title, (cx - title.get_width() // 2, 180))
        self.screen.blit(sub, (cx - sub.get_width() // 2, 290))
        self.screen.blit(ctrl, (cx - ctrl.get_width() // 2, 350))

    def draw_game_over(self, world: object) -> None:
        vencedor = getattr(world, "winner", None)
        if vencedor is not None:
            msg = f"JOGADOR {vencedor} VENCEU!"
            cor_msg = C.PLAYER_COLORS[vencedor]
        else:
            msg = "EMPATE!"
            cor_msg = C.WHITE

        p1_score = world.scores.get(1, 0)
        p2_score = world.scores.get(2, 0)

        title = self.big.render("FIM DE JOGO", True, C.WHITE)
        lbl_winner = self.font.render(msg, True, cor_msg)
        lbl_scores = self.font.render(
            f"J1: {p1_score:04d}     J2: {p2_score:04d}",
            True,
            C.WHITE,
        )
        lbl_restart = self.font.render(
            "Pressione qualquer tecla para reiniciar",
            True,
            C.WHITE,
        )

        cx = C.WIDTH // 2
        self.screen.blit(title, (cx - title.get_width() // 2, 180))
        self.screen.blit(lbl_winner, (cx - lbl_winner.get_width() // 2, 270))
        self.screen.blit(lbl_scores, (cx - lbl_scores.get_width() // 2, 320))
        self.screen.blit(lbl_restart, (cx - lbl_restart.get_width() // 2, 400))
