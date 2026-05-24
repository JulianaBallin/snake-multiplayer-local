"""Mundo do jogo: estado e regras da partida."""

import random
from typing import Dict

from core import config as C
from core.commands import PlayerCommand
from core.entities import Food, PlayerId, Snake, StickyGoo
from core.utils import celula_aleatoria_livre


class World:
    """Estado completo do jogo e logica de atualizacao.

    Recebe comandos indexados por player_id e gera eventos (strings)
    para a camada cliente reagir.
    """

    def __init__(self) -> None:
        self.snakes: Dict[PlayerId, Snake] = {}
        self.foods: list[Food] = []
        self.sticky_goos: list[StickyGoo] = []
        self.scores: Dict[PlayerId, int] = {}
        self.tick_timer = float(C.TICK_INTERVAL)
        self.events: list[str] = []
        self.game_over = False
        self.winner: PlayerId | None = None

        for pid, (start, direction) in C.PLAYER_STARTS.items():
            self.snakes[pid] = Snake(pid, start, direction, C.START_LENGTH)
            self.scores[pid] = 0

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

        self._update_sticky_timers(dt)
        self._update_sticky_goos(dt)

        for pid, cmd in commands.items():
            snake = self.snakes.get(pid)

            if not snake or not snake.alive:
                continue

            if cmd.direction:
                snake.set_direction(cmd.direction)

            if cmd.activate_sticky:
                self._activate_sticky_trail(snake)

        self.tick_timer -= dt

        if self.tick_timer > 0:
            return

        self.tick_timer += float(C.TICK_INTERVAL)
        self._tick()

    def _update_sticky_timers(self, dt: float) -> None:
        for snake in self.snakes.values():
            if snake.sticky_active_timer > 0:
                snake.sticky_active_timer = max(
                    0.0,
                    snake.sticky_active_timer - dt,
                )

    def _update_sticky_goos(self, dt: float) -> None:
        for goo in list(self.sticky_goos):
            goo.lifetime -= dt

            if goo.lifetime <= 0:
                self.sticky_goos.remove(goo)

    def _activate_sticky_trail(self, snake: Snake) -> None:
        if snake.sticky_charges <= 0:
            return

        if snake.sticky_active_timer > 0:
            return

        snake.sticky_charges -= 1
        snake.sticky_active_timer = C.STICKY_ACTIVE_DURATION
        self.events.append("sticky_activated")

    def _add_sticky_goo(
        self,
        pos: tuple[int, int],
        owner_id: PlayerId,
    ) -> None:
        for goo in self.sticky_goos:
            if goo.pos == pos and goo.owner_id == owner_id:
                goo.lifetime = C.STICKY_GOO_DURATION
                return

        self.sticky_goos.append(
            StickyGoo(pos, owner_id, C.STICKY_GOO_DURATION)
        )

    def _spawn_sticky_trail(self, snake: Snake) -> None:
        if snake.sticky_active_timer <= 0:
            return

        for pos in snake.body:
            self._add_sticky_goo(pos, snake.player_id)

    def _is_inside_board(self, pos: tuple[int, int]) -> bool:
        col, row = pos

        return 0 <= col < C.COLS and 0 <= row < C.ROWS

    def _is_on_enemy_sticky_goo(self, snake: Snake) -> bool:
        return any(
            goo.pos == snake.head and goo.owner_id != snake.player_id
            for goo in self.sticky_goos
        )

    def _should_skip_move_by_sticky_slow(self, snake: Snake) -> bool:
        if not self._is_on_enemy_sticky_goo(snake):
            snake.slow_tick_counter = 0
            return False

        snake.slow_tick_counter = (
            snake.slow_tick_counter + 1
        ) % C.STICKY_SLOW_CYCLE

        return snake.slow_tick_counter < C.STICKY_SLOW_SKIPPED_TICKS

    def _nearest_sticky_goo(
        self,
        pos: tuple[int, int],
    ) -> StickyGoo | None:
        px, py = pos
        nearest = None
        nearest_dist = None

        for goo in self.sticky_goos:
            gx, gy = goo.pos
            dist = abs(px - gx) + abs(py - gy)

            if dist > C.STICKY_ATTRACTION_RADIUS:
                continue

            if nearest_dist is None or dist < nearest_dist:
                nearest = goo
                nearest_dist = dist

        return nearest

    def _move_foods_toward_sticky_goos(self) -> None:
        occupied_by_snakes = set()

        for snake in self.snakes.values():
            occupied_by_snakes.update(snake.body)

        occupied_by_foods = {food.pos for food in self.foods}

        for food in self.foods:
            goo = self._nearest_sticky_goo(food.pos)

            if goo is None:
                continue

            fx, fy = food.pos
            gx, gy = goo.pos

            dx = 1 if gx > fx else -1 if gx < fx else 0
            dy = 1 if gy > fy else -1 if gy < fy else 0

            new_pos = (fx + dx, fy + dy)

            if not self._is_inside_board(new_pos):
                continue

            if new_pos in occupied_by_snakes:
                continue

            if new_pos in occupied_by_foods and new_pos != food.pos:
                continue

            occupied_by_foods.discard(food.pos)
            food.pos = new_pos
            occupied_by_foods.add(food.pos)

    def _ocupadas(self) -> set[tuple[int, int]]:
        celulas: set[tuple[int, int]] = set()

        for snake in self.snakes.values():
            celulas.update(snake.body)

        celulas.update(f.pos for f in self.foods)

        return celulas

    def _spawnar_comida(self) -> None:
        pos = celula_aleatoria_livre(self._ocupadas())

        if pos:
            kind = (
                "sticky"
                if random.random() < C.STICKY_ORB_SPAWN_CHANCE
                else "normal"
            )

            self.foods.append(Food(pos, kind))

    def _tick(self) -> None:
        for snake in self.snakes.values():
            if not snake.alive:
                continue

            if self._should_skip_move_by_sticky_slow(snake):
                self.events.append("sticky_slow")
                continue

            snake.move()
            self._spawn_sticky_trail(snake)

        self._move_foods_toward_sticky_goos()

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

                    if food.kind == "sticky":
                        snake.sticky_charges += 1
                        self.events.append("sticky_orb")
                    else:
                        self.scores[snake.player_id] += C.FOOD_VALUE
                        snake.grow += C.GROW_AMOUNT
                        self.events.append("comida")

                    self._spawnar_comida()

        vivas_count = sum(1 for s in self.snakes.values() if s.alive)

        if vivas_count == 0:
            self.game_over = True
            max_score = max(self.scores.values())
            vencedores = [
                p for p, sc in self.scores.items()
                if sc == max_score
            ]
            self.winner = vencedores[0] if len(vencedores) == 1 else None

        elif vivas_count == 1:
            self.game_over = True
            self.winner = next(
                p for p, s in self.snakes.items()
                if s.alive
            )