# -*- coding: utf-8 -*-
"""Константы игры Arcade Game."""
"""Константы игры Arcade Game."""

import arcade

# --- Размеры окна и физика ---
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Arcade Game"
PLAYER_SPEED = 320
BULLET_SPEED = 600
ENEMY_SPEED_MIN = 40
ENEMY_SPEED_MAX = 160
SPAWN_ENEMY_INTERVAL = 1.2
SPAWN_TASK_INTERVAL = 2.5

# --- Цвета (RGB tuples) ---
COLOR_BG = arcade.color.LIGHT_GRAY
COLOR_PLAYER = arcade.color.DARK_BLUE
COLOR_BULLET = arcade.color.YELLOW
COLOR_ENEMY = arcade.color.CRIMSON
COLOR_TASK = arcade.color.APPLE_GREEN
COLOR_UI = arcade.color.DIM_GRAY

# --- Файлы ---
HIGHSCORE_FILE = "highscore.json"
