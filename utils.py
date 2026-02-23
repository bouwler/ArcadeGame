# -*- coding: utf-8 -*-
"""Вспомогательные функции для работы с рекордом."""

import json
import os
from constants import HIGHSCORE_FILE


def load_highscore() -> int:
    """Загрузить рекорд из файла."""
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("highscore", 0))
    except Exception:
        return 0


def save_highscore(score: int):
    """Сохранить рекорд в файл."""
    try:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            json.dump({"highscore": int(score)}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass