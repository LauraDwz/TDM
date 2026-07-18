from model.units.unit import Unit
import settings as s


class Mage(Unit):
    def __init__(self):
        super().__init__(1, 15, 2.0, 0.6, "Mage", s.Color.UNIT_MAGE)
