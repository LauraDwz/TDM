from json import load


def load_levels() -> list[dict]:
    """Charge et retourne la liste des niveaux depuis levels.json"""
    with open("data\level.json", "r", encoding="utf-8") as f:
        data = load(f)
    return data["levels"]


def get_level(index: int) -> dict:
    """Retourne le niveau à l'index donné"""
    levels = load_levels()
    if index < 0 or index >= len(levels):
        raise IndexError(f"Niveau {index} inexistant (0-{len(levels) - 1})")
    return levels[index]
