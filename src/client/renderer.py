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
        # HUD no topo: 4 secoes de largura igual
        secao = C.WIDTH // 4
        for pid in range(1, 5):
            snake = world.snakes.get(pid)
            score = world.scores.get(pid, 0)
            vivo = snake.alive if snake else False
            status = "VIVO" if vivo else "MORTO"
            cor = C.PLAYER_COLORS[pid]
            texto = f"J{pid} {score:04d} [{status}]"
            label = self.font.render(texto, True, cor)
            x = (pid - 1) * secao + 6
            self.screen.blit(label, (x, 5))

    def draw_menu(self) -> None:
        title = self.big.render("SNAKE", True, C.WHITE)
        sub = self.font.render(
            "Pressione qualquer tecla para iniciar",
            True,
            C.WHITE,
        )
        cx = C.WIDTH // 2
        self.screen.blit(title, (cx - title.get_width() // 2, 160))
        self.screen.blit(sub, (cx - sub.get_width() // 2, 260))

        controles = [
            ("J1 (Ciano):", "W A S D"),
            ("J2 (Amarelo):", "Setas"),
            ("J3 (Verde):", "I J K L"),
            ("J4 (Vermelho):", "Num 8 4 2 6"),
        ]
        y = 310
        for nome, teclas in controles:
            pid = int(nome[1])
            cor = C.PLAYER_COLORS[pid]
            label = self.font.render(f"{nome}  {teclas}", True, cor)
            self.screen.blit(label, (cx - label.get_width() // 2, y))
            y += 28

    def draw_game_over(self, world: object) -> None:
        vencedor = getattr(world, "winner", None)
        if vencedor is not None:
            msg = f"JOGADOR {vencedor} VENCEU!"
            cor_msg = C.PLAYER_COLORS[vencedor]
        else:
            msg = "EMPATE!"
            cor_msg = C.WHITE

        title = self.big.render("FIM DE JOGO", True, C.WHITE)
        lbl_winner = self.font.render(msg, True, cor_msg)
        lbl_restart = self.font.render(
            "Pressione qualquer tecla para reiniciar",
            True,
            C.WHITE,
        )

        cx = C.WIDTH // 2
        self.screen.blit(title, (cx - title.get_width() // 2, 140))
        self.screen.blit(lbl_winner, (cx - lbl_winner.get_width() // 2, 230))

        # Placar de todos os jogadores
        y = 280
        for pid in sorted(world.scores.keys()):
            score = world.scores[pid]
            cor = C.PLAYER_COLORS[pid]
            lbl = self.font.render(f"J{pid}: {score:04d} pts", True, cor)
            self.screen.blit(lbl, (cx - lbl.get_width() // 2, y))
            y += 28

        self.screen.blit(lbl_restart, (cx - lbl_restart.get_width() // 2, y + 20))
