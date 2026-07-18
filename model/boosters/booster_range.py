from model.boosters.booster import Booster


class BoosterRange(Booster):
    def __init__(self):
        super().__init__("+Portée", "+1 portée", (40, 140, 200))
