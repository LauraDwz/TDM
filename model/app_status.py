from enum import Enum, auto


class AppStatus(Enum):
    """Définit l'état de la partie, affichant la carte de séléction de niveaux ou en partie."""

    MAP = auto()
    PLAYING = auto()
