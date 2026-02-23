"""Точка входа в игру ArcadeGame."""

from game import ArcadeGame
import arcade


def main():
    window = ArcadeGame()
    arcade.run()


if __name__ == "__main__":
    main()
