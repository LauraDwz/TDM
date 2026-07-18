from model.units.unit import Unit
import settings as s


class Archer(Unit):
    def __init__(self):
        super().__init__(1, 5, 3.0, 1.5, "Archer", s.Color.UNIT_ARCHER)
