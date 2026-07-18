from model.monsters.monster import Monster


class Orc(Monster):
    def __init__(self, path_index: int = 0):
        super().__init__(200, 1.0, 25, "Orc", path_index)
