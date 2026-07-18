import settings as s
from model.cell import Cell, CellType


class Grid:
    def __init__(self, layout: list[list[int]]):
        """Construit la grille à partir d'une matrice d'entiers
        Equivalences : 0 = GRASS, 1 = PATH, 2 = TOWER"""
        self.rows = len(layout)
        self.cols = len(layout[0])
        self.cells: list[list[Cell]] = self._build(layout)

    def _build(self, layout: list[list[int]]) -> list[list[Cell]]:
        link = {
            0: CellType.GRASS,
            1: CellType.PATH,
            2: CellType.TOWER,
        }
        return [
            [Cell(row, col, link[layout[row][col]]) for col in range(self.cols)]
            for row in range(self.rows)
        ]

    def get_cell(self, row: int, col: int) -> Cell | None:
        """Retourne la cellule (row, col) ou None si hors limites"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def get_cell_at_pixel(self, x: int, y: int) -> Cell | None:
        """Retourne la cellule correspondant à une position en pixels (clic souris) ou None si hors limites"""
        col = x // s.CELL_SIZE
        row = y // s.CELL_SIZE
        return self.get_cell(row, col)

    def get_placeable_cells(self) -> list[Cell]:
        """Retourne toutes les cases où une unité peut être posée (cell Type TOWER)"""
        return [cell for row in self.cells for cell in row if cell.unit_placeable]

    def get_path_cells(self) -> list[Cell]:
        """Retourne toutes les cases de chemin (cell type PATH) dans l'ordre de la grille"""
        return [
            cell
            for row in self.cells
            for cell in row
            if cell.cell_type == CellType.PATH
        ]

    def __repr__(self) -> str:
        return f"Grid({self.rows}x{self.cols})"
