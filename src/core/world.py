"""Mundo do jogo: estado e regras da partida."""

from typing import Dict

from core import config as C
from core.commands import PlayerCommand
from core.entities import Food, PlayerId, Snake
from core.utils import celula_aleatoria_livre


class World:
    """Estado completo do jogo e logica de atualizacao.

    Recebe comandos indexados por player_id e gera eventos
    (strings) para a camada cliente reagir.
    """

    def __init__(self) -> None:
        self.snakes: Dict[PlayerId, Snake] = {}
        self.foods: list[Food] = []
        self.scores: Dict[PlayerId, int] = {}
        self.tick_timer = float(C.TICK_INTERVAL)
        self.events: list[str] = []
        self.game_over = False
        self.winner: PlayerId | None = None

        self.snakes[1] = Snake(1, C.P1_START, C.P1_DIR, C.START_LENGTH)
        self.snakes[2] = Snake(2, C.P2_START, C.P2_DIR, C.START_LENGTH)
        self.scores[1] = 0
        self.scores[2] = 0

        for _ in range(C.FOOD_COUNT):
            self._spawnar_comida()

    def reset(self) -> None:
        self.__init__()

    def update(
        self,
        dt: float,
        commands: Dict[PlayerId, PlayerCommand],
    ) -> None:
        self.events.clear()

        if self.game_over:
            return

        for pid, cmd in commands.items():
            snake = self.snakes.get(pid)
            if snake and snake.alive and cmd.direction:
                snake.set_direction(cmd.direction)

        self.tick_timer -= dt
        if self.tick_timer > 0:
            return
        self.tick_timer += float(C.TICK_INTERVAL)

        self._tick()

    def _ocupadas(self) -> set[tuple[int, int]]:
        celulas: set[tuple[int, int]] = set()
        for snake in self.snakes.values():
            celulas.update(snake.body)
        celulas.update(f.pos for f in self.foods)
        return celulas

    def _spawnar_comida(self) -> None:
        pos = celula_aleatoria_livre(self._ocupadas())
        if pos:
            self.foods.append(Food(pos))

    def _tick(self) -> None:
        for snake in self.snakes.values():
            if snake.alive:
                snake.move()

        for snake in self.snakes.values():
            if not snake.alive:
                continue

            hx, hy = snake.head

            if not (0 <= hx < C.COLS and 0 <= hy < C.ROWS):
                snake.alive = False
                self.events.append("morte")
                continue

            corpo = list(snake.body)
            if snake.head in corpo[1:]:
                snake.alive = False
                self.events.append("morte")
                continue

            for outra in self.snakes.values():
                if outra is snake or not outra.alive:
                    continue
                if snake.head in outra.body:
                    snake.alive = False
                    self.events.append("morte")
                    break

        vivas = [s for s in self.snakes.values() if s.alive]
        cabecas = [s.head for s in vivas]
        for snake in vivas:
            if cabecas.count(snake.head) > 1:
                snake.alive = False
                self.events.append("morte")

        for snake in self.snakes.values():
            if not snake.alive:
                continue
            for food in list(self.foods):
                if snake.head == food.pos:
                    self.foods.remove(food)
                    self.scores[snake.player_id] += C.FOOD_VALUE
                    snake.grow += C.GROW_AMOUNT
                    self.events.append("comida")
                    self._spawnar_comida()

        vivas_count = sum(1 for s in self.snakes.values() if s.alive)
        if vivas_count == 0:
            self.game_over = True
            max_score = max(self.scores.values())
            vencedores = [p for p, sc in self.scores.items() if sc == max_score]
            self.winner = vencedores[0] if len(vencedores) == 1 else None
        elif vivas_count == 1:
            self.game_over = True
            self.winner = next(p for p, s in self.snakes.items() if s.alive)
