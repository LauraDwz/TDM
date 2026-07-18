from collections import deque
from model.grid import Grid
from model.cell import Cell, CellType


class PathFinder:
    def calculate_path(self, grid: Grid, start: Cell, end: Cell) -> list[Cell]:
        """Calcule le chemin le plus court entre start et end en BFS. Ne traverse que les cases de type PATH.
        Retourne une liste ordonnée de Cell, ou une liste vide si aucun chemin."""
        queue = deque()
        queue.append(start)
        visited = {(start.row, start.col): None}

        while queue:
            current = queue.popleft()
            if current.row == end.row and current.col == end.col:
                return self._reconstruct(visited, end)
            for neighbor in self._get_neighbors(grid, current):
                key = (neighbor.row, neighbor.col)
                if key not in visited:
                    visited[key] = current
                    queue.append(neighbor)

        return []

    def calculate_paths(
        self, grid: Grid, starts: list[Cell], ends: list[Cell]
    ) -> list[list[Cell]]:
        """Calcule une liste de chemins selon la configuration entrées/sorties :
        - 1 entrée et 1 sortie => 1 chemin  : [E=>S]
        - 2 entrées et 1 sortie => 2 chemins : [E1=>S, E2=>S]
        - 2 entrées et 2 sorties => 2 chemins : [E1=>S1, E2=>S2]
        - 1 entrée et 2 sorties => 2 chemins : [E=>S1, E=>S2]
        """
        if len(starts) == 1 and len(ends) == 1:
            return [self.calculate_path(grid, starts[0], ends[0])]

        if len(starts) == 2 and len(ends) == 1:
            return [
                self.calculate_path(grid, starts[0], ends[0]),
                self.calculate_path(grid, starts[1], ends[0]),
            ]

        if len(starts) == 2 and len(ends) == 2:
            return [
                self.calculate_path(grid, starts[0], ends[0]),
                self.calculate_path(grid, starts[1], ends[1]),
            ]

        if len(starts) == 1 and len(ends) == 2:
            return [
                self.calculate_path(grid, starts[0], ends[0]),
                self.calculate_path(grid, starts[0], ends[1]),
            ]

        raise ValueError(
            f"Configuration non supportée : {len(starts)} entrée(s) / {len(ends)} sortie(s)"
        )

    def _get_neighbors(self, grid: Grid, cell: Cell) -> list[Cell]:
        """Retourne les cases adjacentes (haut, bas, gauche, droite) de type PATH"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            neighbor = grid.get_cell(cell.row + dr, cell.col + dc)
            if neighbor is not None and neighbor.cell_type == CellType.PATH:
                neighbors.append(neighbor)
        return neighbors

    def _reconstruct(self, visited: dict, end: Cell) -> list[Cell]:
        """Remonte le dictionnaire visited pour reconstruire le chemin dans l'ordre"""
        path = []
        current = end
        while current is not None:
            path.append(current)
            key = (current.row, current.col)
            current = visited[key]
        path.reverse()
        return path
