"""Mapeamento de teclado e joystick para comandos de jogador."""

import pygame as pg

from core import config as C
from core.commands import PlayerCommand


_CIMA = (0, -1)
_BAIXO = (0, 1)
_ESQUERDA = (-1, 0)
_DIREITA = (1, 0)

_DEADZONE = 0.5
JOY_BTN_STICKY = 0


KEYMAPS: dict[int, dict[int, tuple[int, int]]] = {
    1: {
        pg.K_i: _CIMA,
        pg.K_k: _BAIXO,
        pg.K_j: _ESQUERDA,
        pg.K_l: _DIREITA,
    },
    2: {
        pg.K_KP8: _CIMA,
        pg.K_KP2: _BAIXO,
        pg.K_KP4: _ESQUERDA,
        pg.K_KP6: _DIREITA,
    },
    3: {
        pg.K_w: _CIMA,
        pg.K_s: _BAIXO,
        pg.K_a: _ESQUERDA,
        pg.K_d: _DIREITA,
    },
    4: {
        pg.K_UP: _CIMA,
        pg.K_DOWN: _BAIXO,
        pg.K_LEFT: _ESQUERDA,
        pg.K_RIGHT: _DIREITA,
    },
}


STICKY_KEYMAPS: dict[int, int] = {
    1: pg.K_u,
    2: pg.K_KP7,
    3: pg.K_q,
    4: pg.K_RCTRL,
}


def _hat_para_direcao(hat: tuple[int, int]) -> tuple[int, int] | None:
    x, y = hat

    if y == 1:
        return _CIMA

    if y == -1:
        return _BAIXO

    if x == -1:
        return _ESQUERDA

    if x == 1:
        return _DIREITA

    return None


def _eixos_para_direcao(ax: float, ay: float) -> tuple[int, int] | None:
    if abs(ax) < _DEADZONE and abs(ay) < _DEADZONE:
        return None

    if abs(ax) >= abs(ay):
        return _DIREITA if ax > 0 else _ESQUERDA

    return _BAIXO if ay > 0 else _CIMA


class InputMapper:
    """Converte eventos de teclado e joystick em PlayerCommand."""

    def __init__(self) -> None:
        pg.joystick.init()
        self._joysticks: dict[int, pg.joystick.JoystickType] = {}
        self._buffer: dict[int, tuple[int, int] | None] = {
            pid: None for pid in KEYMAPS
        }
        self._sticky_buffer: dict[int, bool] = {
            pid: False for pid in KEYMAPS
        }
        self._pausar_pendente = False
        self._inicializar_joysticks()

    def processar_evento(self, event: pg.event.Event) -> None:
        self._processar_teclado(event)
        self._processar_joystick_evento(event)

    def gerar_comandos(self) -> dict[int, PlayerCommand]:
        self._processar_analogicos()

        comandos = {
            pid: PlayerCommand(
                direction=self._buffer[pid],
                activate_sticky=self._sticky_buffer[pid],
            )
            for pid in KEYMAPS
        }

        self._buffer = {pid: None for pid in KEYMAPS}
        self._sticky_buffer = {pid: False for pid in KEYMAPS}

        return comandos

    def consumir_pausa(self) -> bool:
        acionado = self._pausar_pendente
        self._pausar_pendente = False

        return acionado

    def status_joysticks(self) -> dict[int, str | None]:
        status: dict[int, str | None] = {pid: None for pid in KEYMAPS}

        for joy_id, joy in self._joysticks.items():
            slot = self._slot_do_joystick(joy_id)

            if slot is not None:
                status[slot] = joy.get_name()

        return status

    def _processar_teclado(self, event: pg.event.Event) -> None:
        if event.type != pg.KEYDOWN:
            return

        for pid, mapa in KEYMAPS.items():
            if event.key in mapa:
                self._buffer[pid] = mapa[event.key]

        for pid, key in STICKY_KEYMAPS.items():
            if event.key == key:
                self._sticky_buffer[pid] = True

    def _inicializar_joysticks(self) -> None:
        for i in range(pg.joystick.get_count()):
            joy = pg.joystick.Joystick(i)
            joy.init()
            self._joysticks[i] = joy

    def _slot_do_joystick(self, joy_id: int) -> int | None:
        slot = joy_id + 1

        return slot if slot in KEYMAPS else None

    def _processar_joystick_evento(self, event: pg.event.Event) -> None:
        if event.type == pg.JOYDEVICEADDED:
            joy = pg.joystick.Joystick(event.device_index)
            joy.init()
            self._joysticks[event.device_index] = joy
            return

        if event.type == pg.JOYDEVICEREMOVED:
            self._joysticks.pop(event.instance_id, None)
            return

        if event.type == pg.JOYHATMOTION:
            pid = self._slot_do_joystick(event.joy)

            if pid is None:
                return

            direcao = _hat_para_direcao(event.value)

            if direcao:
                self._buffer[pid] = direcao
            return

        if event.type == pg.JOYBUTTONDOWN:
            pid = self._slot_do_joystick(event.joy)

            if pid is None:
                return

            if event.button == JOY_BTN_STICKY:
                self._sticky_buffer[pid] = True

            if event.button in C.JOY_BTNS_PAUSE:
                self._pausar_pendente = True

    def _processar_analogicos(self) -> None:
        for joy_id, joy in self._joysticks.items():
            pid = self._slot_do_joystick(joy_id)

            if pid is None or self._buffer[pid] is not None:
                continue

            if joy.get_numaxes() < 2:
                continue

            direcao = _eixos_para_direcao(
                joy.get_axis(0),
                joy.get_axis(1),
            )

            if direcao:
                self._buffer[pid] = direcao