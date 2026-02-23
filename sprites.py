# -*- coding: utf-8 -*-
"""Классы игровых спрайтов."""

import arcade
import random
import math
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_SPEED, BULLET_SPEED,
    COLOR_PLAYER, COLOR_BULLET, COLOR_ENEMY, COLOR_TASK
)


class Player(arcade.SpriteSolidColor):
    """Игрок — прямоугольник, который может двигаться и стрелять."""

    def __init__(self, x: float, y: float):
        super().__init__(44, 54, color=COLOR_PLAYER)
        self.center_x = x
        self.center_y = y
        self.change_x = 0.0
        self.change_y = 0.0
        self.move_speed = PLAYER_SPEED
        self.hp = 5
        self.max_hp = 5
        self.score = 0
        self.level = 1
        self.shot_cooldown = 0.20
        self._shot_timer = 0.0

    def update_movement(self, dt: float):
        """Обновление позиции игрока по скорости и dt."""
        self.center_x += self.change_x * dt
        self.center_y += self.change_y * dt
        # Ограничение по экрану
        half_w, half_h = self.width / 2, self.height / 2
        self.center_x = max(half_w, min(SCREEN_WIDTH - half_w, self.center_x))
        self.center_y = max(half_h, min(SCREEN_HEIGHT - half_h, self.center_y))
        if self._shot_timer > 0:
            self._shot_timer -= dt

    def can_shoot(self) -> bool:
        return self._shot_timer <= 0

    def shoot(self):
        self._shot_timer = self.shot_cooldown


class Bullet(arcade.SpriteSolidColor):
    """Пуля фокуса, летит вверх."""

    def __init__(self, x: float, y: float):
        super().__init__(8, 16, color=COLOR_BULLET)
        self.center_x = x
        self.center_y = y
        self.speed = BULLET_SPEED

    def update(self, dt: float = 1/60):
        self.center_y += self.speed * dt
        # если выше экрана — пометим для удаления (arcade сделает сама проверку коллекций)


class Enemy(arcade.SpriteSolidColor):
    """Дистрактор — вражина, летит вниз и бьёт игрока при контакте."""

    def __init__(self, x: float, y: float, speed: float):
        super().__init__(40, 34, color=COLOR_ENEMY)
        self.center_x = x
        self.center_y = y
        self.speed = speed
        # небольшая горизонтальная дрейф-скорость
        self.drift = random.uniform(-40, 40)

    def update(self, dt: float = 1 / 60):
        self.center_y -= self.speed * dt
        self.center_x += self.drift * dt
        # ограничение по краям
        half_w = self.width / 2
        if self.center_x < half_w:
            self.center_x = half_w
            self.drift *= -1
        if self.center_x > SCREEN_WIDTH - half_w:
            self.center_x = SCREEN_WIDTH - half_w
            self.drift *= -1


class TaskItem(arcade.SpriteSolidColor):
    """Полезная задача — предмет, собираемый игроком."""

    def __init__(self, x: float, y: float, value: int = 10):
        super().__init__(28, 22, color=COLOR_TASK)
        self.center_x = x
        self.center_y = y
        self.value = value
        # плавающая анимация
        self._float_phase = random.random() * 3.14

    def update(self, dt: float = 1 / 60):
        # плавает по вертикали слегка
        self._float_phase += dt * 3.0
        offset = 4.0 * (0.5 - abs(math.sin(self._float_phase)))
        self.center_y += offset