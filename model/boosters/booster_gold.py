from model.boosters.booster import Booster


class BoosterGold(Booster):
    def __init__(self):
        super().__init__("Or", "50 x vagues", (180, 150, 20))

    def activate(self) -> None:
        """Méthode de la classe mère redéfinie car un booster GOLD ne reste pas activé contrairement aux autres"""
        self.used = True
