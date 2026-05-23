"""Renderizacao das cenas do jogo."""

import pygame as pg

from core import config as C
from core.entities import Food, Snake

_MARGEM_CORPO = 2
_MARGEM_COMIDA = 4
_RAIO_BORDA = 5
_RAIO_PAINEL = 8
_COR_PAINEL_BG = (12, 12, 12)

_LAYOUTS: dict[int, list[tuple[str, int, int]]] = {
    1: [("I", 1, 0), ("J", 0, 1), ("K", 1, 1), ("L", 2, 1)],
    2: [("8", 1, 0), ("4", 0, 1), ("2", 1, 2), ("6", 2, 1)],
    3: [("W", 1, 0), ("A", 0, 1), ("S", 1, 1), ("D", 2, 1)],
    4: [("\u2191", 1, 0), ("\u2190", 0, 1), ("\u2193", 1, 1), ("\u2192", 2, 1)],
}

_NOME_COR = {1: "AZUL", 2: "AMARELO", 3: "VERDE", 4: "VERMELHO"}


class Renderer:
    """Desenha o estado do jogo na superficie pygame."""

    def __init__(
        self,
        tela: pg.Surface,
        fontes: dict[str, pg.font.Font],
    ) -> None:
        self._tela = tela
        self._fonte = fontes["normal"]
        self._fonte_grande = fontes["grande"]
        self._fonte_pequena = fontes["pequena"]

    def limpar(self) -> None:
        self._tela.fill(C.BLACK)

    def desenhar_mundo(self, world: object) -> None:
        self._desenhar_grade()
        for food in world.foods:
            self._desenhar_comida(food)
        for snake in world.snakes.values():
            if snake.alive:
                self._desenhar_cobra(snake)

    def desenhar_hud(self, world: object) -> None:
        sec = C.WIDTH // 4
        for pid in range(1, 5):
            snake = world.snakes.get(pid)
            pontos = world.scores.get(pid, 0)
            status = "VIVO" if (snake and snake.alive) else "MORTO"
            label = self._fonte.render(
                f"J{pid} {pontos:04d} [{status}]", True, C.PLAYER_COLORS[pid]
            )
            self._tela.blit(label, ((pid - 1) * sec + 6, 5))

    def desenhar_menu(self, status_joy: dict[int, str | None]) -> None:
        cx = C.WIDTH // 2

        titulo = self._fonte_grande.render("SNAKE", True, C.WHITE)
        self._tela.blit(titulo, (cx - titulo.get_width() // 2, 14))

        sub = self._fonte.render(
            "MULTIPLAYER LOCAL  \u2014  4 JOGADORES", True, (140, 140, 140)
        )
        self._tela.blit(sub, (cx - sub.get_width() // 2, 93))

        posicoes = [(1, 15, 126), (2, 413, 126), (3, 15, 320), (4, 413, 320)]
        for pid, px, py in posicoes:
            self._desenhar_painel(pid, px, py, status_joy.get(pid))

        total = sum(1 for v in status_joy.values() if v is not None)
        if total:
            txt_joy = f"[ {total} joystick(s) detectado(s) ]"
            cor_joy = (80, 200, 80)
        else:
            txt_joy = "[ Nenhum joystick detectado  \u2014  use o teclado ]"
            cor_joy = (90, 90, 90)

        lbl_joy = self._fonte.render(txt_joy, True, cor_joy)
        lbl_start = self._fonte.render(
            "Pressione qualquer tecla para iniciar", True, C.WHITE
        )
        self._tela.blit(lbl_joy, (cx - lbl_joy.get_width() // 2, 519))
        self._tela.blit(lbl_start, (cx - lbl_start.get_width() // 2, 556))

    def desenhar_fim_de_jogo(self, world: object) -> None:
        cx = C.WIDTH // 2
        vencedor = getattr(world, "winner", None)

        if vencedor:
            cor_v = C.PLAYER_COLORS[vencedor]
            faixa = pg.Surface((C.WIDTH, 88), pg.SRCALPHA)
            faixa.fill((cor_v[0], cor_v[1], cor_v[2], 22))
            self._tela.blit(faixa, (0, 36))

        titulo = self._fonte_grande.render("FIM DE JOGO", True, C.WHITE)
        self._tela.blit(titulo, (cx - titulo.get_width() // 2, 36))

        if vencedor:
            msg = f"JOGADOR  {vencedor}  VENCEU!"
            cor_msg = C.PLAYER_COLORS[vencedor]
        else:
            msg = "E M P A T E"
            cor_msg = C.WHITE

        lbl_v = self._fonte.render(msg, True, cor_msg)
        self._tela.blit(lbl_v, (cx - lbl_v.get_width() // 2, 146))

        y = 198
        pg.draw.line(self._tela, (60, 60, 60), (cx - 180, y), (cx + 180, y), 1)
        y += 14

        for pid in sorted(world.scores):
            pontos = world.scores[pid]
            cor = C.PLAYER_COLORS[pid]
            eh_venc = pid == vencedor

            if eh_venc:
                hl = pg.Surface((360, 32), pg.SRCALPHA)
                hl.fill((cor[0], cor[1], cor[2], 35))
                self._tela.blit(hl, (cx - 180, y - 3))

            sufixo = "  \u25c4 VENCEDOR" if eh_venc else ""
            linha = self._fonte.render(
                f"J{pid}:  {pontos:04d} pts{sufixo}", True, cor
            )
            self._tela.blit(linha, (cx - linha.get_width() // 2, y))
            y += 34

        pg.draw.line(self._tela, (60, 60, 60), (cx - 180, y + 2), (cx + 180, y + 2), 1)

        lbl_r = self._fonte.render(
            "Pressione qualquer tecla para reiniciar", True, (150, 150, 150)
        )
        self._tela.blit(lbl_r, (cx - lbl_r.get_width() // 2, y + 22))

    def _desenhar_painel(
        self, pid: int, x: int, y: int, joy_nome: str | None
    ) -> None:
        cor = C.PLAYER_COLORS[pid]
        w, h = 372, 184

        pg.draw.rect(self._tela, _COR_PAINEL_BG, (x, y, w, h), border_radius=_RAIO_PAINEL)
        pg.draw.rect(self._tela, cor, (x, y, w, h), width=2, border_radius=_RAIO_PAINEL)

        cab = self._fonte.render(
            f"\u25cf JOGADOR {pid}  \u2014  {_NOME_COR[pid]}", True, cor
        )
        self._tela.blit(cab, (x + 12, y + 10))

        pg.draw.line(self._tela, cor, (x + 8, y + 37), (x + w - 8, y + 37), 1)

        tec = self._fonte_pequena.render("TECLADO:", True, (140, 140, 140))
        self._tela.blit(tec, (x + 12, y + 45))

        self._desenhar_mini_teclado(pid, x + 100, y + 58)

        if joy_nome:
            j_txt = f">> {joy_nome[:32]}"
            j_cor = (80, 210, 80)
        else:
            j_txt = "Joystick nao conectado"
            j_cor = (75, 75, 75)

        jlbl = self._fonte_pequena.render(j_txt, True, j_cor)
        self._tela.blit(jlbl, (x + 12, y + 160))

    def _desenhar_mini_teclado(self, pid: int, ox: int, oy: int) -> None:
        cor = C.PLAYER_COLORS[pid]
        tam, esp = 26, 30

        for label, col, row in _LAYOUTS[pid]:
            rx = ox + col * esp
            ry = oy + row * esp
            rect = pg.Rect(rx, ry, tam, tam)
            pg.draw.rect(self._tela, (35, 35, 35), rect, border_radius=5)
            pg.draw.rect(self._tela, cor, rect, width=1, border_radius=5)
            txt = self._fonte_pequena.render(label, True, C.WHITE)
            self._tela.blit(txt, (
                rx + tam // 2 - txt.get_width() // 2,
                ry + tam // 2 - txt.get_height() // 2,
            ))

    def _desenhar_grade(self) -> None:
        for col in range(C.COLS + 1):
            pg.draw.line(self._tela, C.GRID_COLOR,
                         (col * C.CELL, 0), (col * C.CELL, C.HEIGHT))
        for row in range(C.ROWS + 1):
            pg.draw.line(self._tela, C.GRID_COLOR,
                         (0, row * C.CELL), (C.WIDTH, row * C.CELL))

    def _desenhar_cobra(self, snake: Snake) -> None:
        cor_corpo = C.PLAYER_COLORS[snake.player_id]
        cor_cabeca = C.PLAYER_HEAD_COLORS[snake.player_id]
        for i, (col, row) in enumerate(snake.body):
            cor = cor_cabeca if i == 0 else cor_corpo
            rect = pg.Rect(
                col * C.CELL + _MARGEM_CORPO,
                row * C.CELL + _MARGEM_CORPO,
                C.CELL - _MARGEM_CORPO * 2,
                C.CELL - _MARGEM_CORPO * 2,
            )
            pg.draw.rect(self._tela, cor, rect, border_radius=_RAIO_BORDA)

    def _desenhar_comida(self, food: Food) -> None:
        col, row = food.pos
        rect = pg.Rect(
            col * C.CELL + _MARGEM_COMIDA,
            row * C.CELL + _MARGEM_COMIDA,
            C.CELL - _MARGEM_COMIDA * 2,
            C.CELL - _MARGEM_COMIDA * 2,
        )
        pg.draw.ellipse(self._tela, C.FOOD_COLOR, rect)
