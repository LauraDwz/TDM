from model.boosters.booster import Booster


class BoosterSpeed(Booster):
    def __init__(self):
        super().__init__("+Vitesse", "+20% vitesse", (60, 180, 100))
