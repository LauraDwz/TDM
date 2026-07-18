from model.monsters.monster import Monster


class Goblin(Monster):
    def __init__(self, path_index: int = 0):
        super().__init__(60, 2.5, 10, "Goblin", path_index)
