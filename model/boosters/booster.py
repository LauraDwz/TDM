class Booster:
    """Il existe 4 types de boosters  :
    => GOLD qui donne de l'or immédiatement
    => RANGE qui augmente la portée des unités
    => ATTACK qui augmente les dégats des unités de 20%
    => ATTACK_SPEED qui augmente de 20% la vitesse d'attaque
    Ces trois derniers durent jusqu'à la fin de la vague"""

    def __init__(self, label: str, description: str, color: tuple):
        self.used = False
        self.active = False
        self.label = label
        self.description = description
        self.color = color

    @property
    def available(self) -> bool:
        return not self.used and not self.active

    def activate(self) -> None:
        self.used = True
        self.active = True

    def desactivate(self) -> None:
        self.active = False
