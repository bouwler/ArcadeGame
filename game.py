# -*- coding: utf-8 -*-
"""Главный класс игры Arcade Game."""

import arcade
import random
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
    COLOR_BG, COLOR_UI,
    SPAWN_ENEMY_INTERVAL, SPAWN_TASK_INTERVAL,
    ENEMY_SPEED_MIN, ENEMY_SPEED_MAX
)
from sprites import Player, Bullet, Enemy, TaskItem
from utils import load_highscore, save_highscore


class ArcadeGame(arcade.Window):
    """Главный контроллер игры: меню, логика, рендер, события."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(COLOR_BG)

        # игровые группы спрайтов
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.task_list = arcade.SpriteList()

        # игрок
        self.player = Player(SCREEN_WIDTH / 2, 120)
        self.player_list.append(self.player)

        # таймеры спавна
        self._enemy_spawn_timer = SPAWN_ENEMY_INTERVAL
        self._task_spawn_timer = SPAWN_TASK_INTERVAL

        # состояние окна / сцена
        self._state = "menu"  # menu | playing | paused | gameover

        # рекорд
        self.highscore = load_highscore()

        # шрифты и UI
        self.ui_font = "Arial"

        # для плавного движения клавиш
        self._keys = {"left": False, "right": False, "up": False, "down": False}

        # начальные параметры
        self.set_vsync(True)
        print("Arcade Game готов. Управление: WASD/стрелки — движение; ПРОБЕЛ — выстрел; P — пауза")

    # --- Основные циклы arcade ---
    def on_draw(self):
        """Отрисовка в зависимости от состояния игры."""
        self.clear()
        if self._state == "menu":
            self._draw_menu()
        elif self._state == "playing":
            self._draw_game()
        elif self._state == "paused":
            self._draw_game()
            self._draw_pause()
        elif self._state == "gameover":
            self._draw_game()
            self._draw_gameover()

    # --- Рендер сцены ---
    def _draw_game(self):
        """Отрисовка игрового мира: спрайты, HUD."""
        # спрайты
        self.task_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        # HUD слева — очки и уровень
        arcade.draw_text(f"Очки: {self.player.score}", 12, SCREEN_HEIGHT - 28,
                         COLOR_UI, 18, font_name=self.ui_font)
        arcade.draw_text(f"Уровень: {self.player.level}", 12, SCREEN_HEIGHT - 54,
                         COLOR_UI, 14, font_name=self.ui_font)

        # HP справа
        hp_text = f"HP: {self.player.hp}/{self.player.max_hp}"
        arcade.draw_text(hp_text, SCREEN_WIDTH - 140, SCREEN_HEIGHT - 28,
                         COLOR_UI, 18, font_name=self.ui_font)

        # рекорд
        arcade.draw_text(f"Рекорд: {self.highscore}", SCREEN_WIDTH - 240, SCREEN_HEIGHT - 54,
                         COLOR_UI, 14, font_name=self.ui_font)

        # подсказка внизу
        arcade.draw_text("Пробел — стрелять. P — пауза. Esc — меню",
                         12, 8, COLOR_UI, 12, font_name=self.ui_font)

    def _draw_menu(self):
        """Отрисовка меню."""
        arcade.draw_text("Arcade Game", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.72,
                         COLOR_UI, 48, anchor_x="center", font_name=self.ui_font)
        arcade.draw_text("1 — Начать игру", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.52,
                         COLOR_UI, 20, anchor_x="center", font_name=self.ui_font)
        arcade.draw_text("2 — Рекорд", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.46,
                         COLOR_UI, 18, anchor_x="center", font_name=self.ui_font)
        arcade.draw_text("3 — Выйти", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.40,
                         COLOR_UI, 18, anchor_x="center", font_name=self.ui_font)
        # Отображение рекорда
        arcade.draw_text(f"Текущий рекорд: {self.highscore}",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.34,
                         COLOR_UI, 16, anchor_x="center", font_name=self.ui_font)
        arcade.draw_text("WASD / стрелки — движение, пробел — стрелять",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.26,
                         COLOR_UI, 12, anchor_x="center", font_name=self.ui_font)

    def _draw_pause(self):
        """Отрисовка наложения паузы."""
        left = SCREEN_WIDTH / 2 - 260
        bottom = SCREEN_HEIGHT / 2 - 110
        arcade.draw_lbwh_rectangle_filled(left, bottom, 520, 220,
                                          (240, 240, 240, 200))
        arcade.draw_text("ПАУЗА", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 24,
                         COLOR_UI, 36, anchor_x="center", font_name=self.ui_font)
        arcade.draw_text("P — продолжить, Esc — меню",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 18,
                         COLOR_UI, 14, anchor_x="center", font_name=self.ui_font)

    def _draw_gameover(self):
        """Отрисовка экрана окончания игры."""
        left = SCREEN_WIDTH / 2 - 310
        bottom = SCREEN_HEIGHT / 2 - 160
        arcade.draw_lbwh_rectangle_filled(left, bottom, 620, 320,
                                          (255, 255, 255, 240))
        arcade.draw_text("Игра окончена", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80,
                         COLOR_UI, 36, anchor_x="center", font_name=self.ui_font)
        arcade.draw_text(f"Твой счёт: {self.player.score}",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20,
                         COLOR_UI, 20, anchor_x="center", font_name=self.ui_font)
        arcade.draw_text("Нажми 1 — сыграть снова, Esc — выйти",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 36,
                         COLOR_UI, 16, anchor_x="center", font_name=self.ui_font)

    # --- Обработчики ввода ---
    def on_key_press(self, symbol, modifiers):
        """Обработка нажатий клавиш."""
        if self._state == "menu":
            if symbol == arcade.key.KEY_1 or symbol == arcade.key.NUM_1:
                self._start_game()
            elif symbol == arcade.key.KEY_2 or symbol == arcade.key.NUM_2:
                self._show_highscore_popup()
            elif symbol == arcade.key.KEY_3 or symbol == arcade.key.NUM_3 or symbol == arcade.key.ESCAPE:
                arcade.close_window()
            return

        if self._state == "playing":
            if symbol in (arcade.key.W, arcade.key.UP):
                self._keys["up"] = True
            if symbol in (arcade.key.S, arcade.key.DOWN):
                self._keys["down"] = True
            if symbol in (arcade.key.A, arcade.key.LEFT):
                self._keys["left"] = True
            if symbol in (arcade.key.D, arcade.key.RIGHT):
                self._keys["right"] = True
            if symbol == arcade.key.SPACE:
                self._player_shoot()
            if symbol == arcade.key.P:
                self._state = "paused"
            if symbol == arcade.key.ESCAPE:
                self._state = "menu"
            return

        if self._state == "paused":
            if symbol == arcade.key.P:
                self._state = "playing"
            if symbol == arcade.key.ESCAPE:
                self._state = "menu"
            return

        if self._state == "gameover":
            if symbol == arcade.key.KEY_1 or symbol == arcade.key.NUM_1:
                self._start_game()
            if symbol == arcade.key.ESCAPE:
                arcade.close_window()

    def on_key_release(self, symbol, modifiers):
        """Обработка отпусканий клавиш."""
        if symbol in (arcade.key.W, arcade.key.UP):
            self._keys["up"] = False
        if symbol in (arcade.key.S, arcade.key.DOWN):
            self._keys["down"] = False
        if symbol in (arcade.key.A, arcade.key.LEFT):
            self._keys["left"] = False
        if symbol in (arcade.key.D, arcade.key.RIGHT):
            self._keys["right"] = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Клик мышью делает выстрел."""
        if self._state == "playing":
            self._player_shoot()

    def on_update(self, delta_time: float):
        """Главная логика обновления игры."""
        if self._state == "playing":
            self._update_playing(delta_time)

    # --- Игровая логика ---
    def _start_game(self):
        """Запустить новую игру: сбросить мир и параметры."""
        # очистка списков
        self.bullet_list.clear()
        self.enemy_list.clear()
        self.task_list.clear()
        # сброс игрока
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = 120
        self.player.hp = self.player.max_hp
        self.player.score = 0
        self.player.level = 1
        self.player._shot_timer = 0.0
        # таймеры
        self._enemy_spawn_timer = SPAWN_ENEMY_INTERVAL
        self._task_spawn_timer = SPAWN_TASK_INTERVAL
        self._state = "playing"

    def _player_shoot(self):
        """Создать пулю из позиции игрока, если можно стрелять."""
        if not self.player.can_shoot():
            return
        bullet = Bullet(self.player.center_x,
                        self.player.center_y + self.player.height / 2 + 6)
        self.bullet_list.append(bullet)
        self.player.shoot()

    def _spawn_enemy(self):
        """Спавн врага сверху с рандомной скоростью и координатой."""
        x = random.uniform(40, SCREEN_WIDTH - 40)
        y = SCREEN_HEIGHT + 40
        speed = random.uniform(
            ENEMY_SPEED_MIN + (self.player.level - 1) * 4,
            ENEMY_SPEED_MAX + (self.player.level - 1) * 8
        )
        enemy = Enemy(x, y, speed)
        self.enemy_list.append(enemy)

    def _spawn_task(self):
        """Спавн полезного предмета (задача)."""
        x = random.uniform(30, SCREEN_WIDTH - 30)
        y = SCREEN_HEIGHT + 24
        value = 10 + (self.player.level - 1) * 2
        task = TaskItem(x, y, value)
        self.task_list.append(task)

    def _update_playing(self, dt: float):
        """Обновление логики в состоянии PLAYING."""
        # движение игрока по нажатым клавишам
        vx = 0
        vy = 0
        if self._keys["left"]:
            vx -= 1
        if self._keys["right"]:
            vx += 1
        if self._keys["up"]:
            vy += 1
        if self._keys["down"]:
            vy -= 1
        # нормализуем диагональное движение
        if vx != 0 and vy != 0:
            vx *= 0.7071
            vy *= 0.7071
        self.player.change_x = vx * self.player.move_speed
        self.player.change_y = vy * self.player.move_speed
        self.player.update_movement(dt)

        # обновление всех спрайтов
        self.bullet_list.update(dt)
        self.enemy_list.update(dt)
        self.task_list.update(dt)

        # удаляем пули выше экрана
        for b in list(self.bullet_list):
            if b.center_y > SCREEN_HEIGHT + 20:
                b.remove_from_sprite_lists()

        # удаляем врагов ниже экрана и урон игроку
        for e in list(self.enemy_list):
            if e.center_y < -40:
                e.remove_from_sprite_lists()
                # штраф очков, если упустил врага
                self.player.score = max(0, self.player.score - 5)

        # удаляем задачи ниже экрана
        for t in list(self.task_list):
            if t.center_y < -40:
                t.remove_from_sprite_lists()

        # спавн врагов и задач по таймеру
        self._enemy_spawn_timer -= dt
        self._task_spawn_timer -= dt
        if self._enemy_spawn_timer <= 0:
            self._spawn_enemy()
            self._enemy_spawn_timer = max(0.4,
                                          SPAWN_ENEMY_INTERVAL - (self.player.level - 1) * 0.05)
        if self._task_spawn_timer <= 0:
            self._spawn_task()
            self._task_spawn_timer = max(0.8,
                                         SPAWN_TASK_INTERVAL - (self.player.level - 1) * 0.07)

        # столкновения: пули <-> враги
        for bullet in list(self.bullet_list):
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
                    self.player.score += 8 + (self.player.level - 1)

        # столкновения: игрок <-> враги
        hit_enemies = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        if hit_enemies:
            for e in hit_enemies:
                e.remove_from_sprite_lists()
                self.player.hp -= 1

        # столкновения: игрок <-> задачи
        hit_tasks = arcade.check_for_collision_with_list(self.player, self.task_list)
        if hit_tasks:
            for t in hit_tasks:
                self.player.score += t.value
                t.remove_from_sprite_lists()
                # лёгкая прогрессия: каждые 200 очков — уровень
                if self.player.score // 200 + 1 > self.player.level:
                    self.player.level += 1
                    # лечим игрока немного при повышении уровня
                    self.player.hp = min(self.player.max_hp, self.player.hp + 1)

        # если здоровье упало — конец игры
        if self.player.hp <= 0:
            self._game_over()

    def _game_over(self):
        """Обработка завершения игры: сохранение рекорда и переход в state."""
        # проверяем рекорд
        if self.player.score > self.highscore:
            self.highscore = self.player.score
            save_highscore(self.highscore)
        self._state = "gameover"

    def _show_highscore_popup(self):
        """Показать рекорд (в консоль)."""
        print(f"Рекорд: {self.highscore}")
