from model.boosters.booster import Booster


class BoosterAttack(Booster):
    def __init__(self):
        super().__init__("+Attaque", "+20% dégats", (200, 60, 60))
