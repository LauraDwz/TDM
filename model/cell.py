import settings as s
from enum import Enum, auto


class CellType(Enum):
    GRASS = auto()
    PATH = auto()
    TOWER = auto()


class Cell:
    def __init__(self, row: int, col: int, cell_type: CellType):
        self.row = row
        self.col = col
        self.cell_type = cell_type
        self.unit = None

    @property
    def unit_placeable(self) -> bool:
        """Une unité peut être posée ici si la case est de type TOWER et libre."""
        return self.cell_type == CellType.TOWER and self.unit is None

    @property
    def pixel_x(self) -> int:
        """Coordonnée X en pixels du coin supérieur gauche de la case."""
        return self.col * s.CELL_SIZE

    @property
    def pixel_y(self) -> int:
        """Coordonnée Y en pixels du coin supérieur gauche de la case."""
        return self.row * s.CELL_SIZE

    def __repr__(self) -> str:
        return f"Cell(row={self.row}, col={self.col}, type={self.cell_type.name})"
