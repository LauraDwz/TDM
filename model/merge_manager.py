from model.units.unit import Unit
import settings as s


class MergeManager:
    def can_merge(self, unit1: Unit, unit2: Unit) -> bool:
        """Vérifie que deux unités peuvent fusionner, donc si elles sont du même type, ont le même niveau et n'ont pas atteint le niveau maximum"""
        return (
            type(unit1) is type(unit2)
            and unit1.level == unit2.level
            and unit1.level < s.MAX_UNIT_LEVEL
        )

    def merge(self, unit1: Unit, unit2: Unit) -> Unit:
        """Fusionne deux unités en vérifiant leur compatibilité. Conserve unit1, lui applique level_up, et retourne l'unité résultante.
        unit2 doit être retirée de la grille par le controller"""
        if not self.can_merge(unit1, unit2):
            raise ValueError(f"Fusion impossible entre {unit1} et {unit2}.")
        unit1.level_up()
        return unit1
