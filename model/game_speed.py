from enum import Enum, auto


class GameSpeed(Enum):
    """Classe qui permet d'avoir différentes vitesses de jeu
    SLOW vitesse x0.5, NORMAL vitesse x1, FAST vitesse x1.5
    Gérable par le joueur via le bouton dans le HUD"""

    SLOW = auto()
    NORMAL = auto()
    FAST = auto()

    def get_speed(self) -> float:
        if self == GameSpeed.SLOW:
            return 0.5
        if self == GameSpeed.NORMAL:
            return 1.0
        return 1.5

    def change(self) -> "GameSpeed":
        """Renvoie le prochain selon le cycle"""
        cycle = [GameSpeed.NORMAL, GameSpeed.FAST, GameSpeed.SLOW]
        index = cycle.index(self)
        return cycle[(index + 1) % len(cycle)]

    def triangle_count(self) -> int:
        """Renvoie le nombre de triangles pour l'affichage de l'icône"""
        match self:
            case GameSpeed.SLOW:
                return 1
            case GameSpeed.NORMAL:
                return 2
        return 3
