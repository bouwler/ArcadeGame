#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Точка входа в игру TaskRunner."""

from game import TaskRunnerGame
import arcade


def main():
    window = TaskRunnerGame()
    arcade.run()


if __name__ == "__main__":
    main()