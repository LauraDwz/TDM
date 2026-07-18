from enum import Enum, auto


class GameStatus(Enum):
    PLAYING = auto()
    MENU = auto()
    INFO = auto()
    GAME_OVER = auto()
    VICTORY = auto()
