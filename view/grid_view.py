import pygame
from model.grid import Grid
from model.cell import Cell, CellType
import settings as s

_GRASS_BASE = (45, 100, 45)
_GRASS_DARK = (35, 80, 35)
_GRASS_BLADE = (60, 130, 60)

_PATH_BASE = (160, 130, 80)
_PATH_PEBBLE = (140, 110, 65)
_PATH_PEBBLE_LIGHT = (180, 155, 100)

_TARMAC_BASE = (55, 55, 65)
_TARMAC_MARK = (70, 70, 82)

_PORTAL_OUTER = (100, 60, 180)
_PORTAL_INNER = (180, 120, 255)
_PORTAL_GLOW = (220, 180, 255)


class GridView:
    def __init__(self):
        self._grass_surface = None
        self._path_surface = None
        self._tarmac_surface = None
        self._end_surface = None
        self._portal_surface = None
        self._cell_size = None
        self._prerender(s.CELL_SIZE)

    def _prerender(self, size: int) -> None:
        """Génère une fois les surfaces texturées pour chaque type de case"""
        self._cell_size = size
        self._grass_surface = self._make_grass(size)
        self._path_surface = self._make_path(size)
        self._tarmac_surface = self._make_tarmac(size)
        self._end_surface = self._make_end(size)
        self._portal_surface = self._make_portal(size)

    def _make_grass(self, size: int) -> pygame.Surface:
        surface = pygame.Surface((size, size))
        surface.fill(_GRASS_BASE)
        rng = _SeededRng(42)
        for _ in range(18):
            px = rng.next_int(size)
            py = rng.next_int(size)
            r = rng.next_int(10) + 6
            shade = _GRASS_DARK if rng.next_int(2) == 0 else _GRASS_BASE
            pygame.draw.circle(surface, shade, (px, py), r)
        for _ in range(12):
            bx = rng.next_int(size - 4) + 2
            by = rng.next_int(size - 6) + 4
            pygame.draw.line(surface, _GRASS_BLADE, (bx, by), (bx - 2, by - 5), 1)
            pygame.draw.line(surface, _GRASS_BLADE, (bx, by), (bx + 2, by - 5), 1)
        return surface

    def _make_path(self, size: int) -> pygame.Surface:
        surface = pygame.Surface((size, size))
        surface.fill(_PATH_BASE)
        rng = _SeededRng(7)
        for _ in range(8):
            px = rng.next_int(size - 6) + 3
            py = rng.next_int(size - 6) + 3
            rw = rng.next_int(5) + 3
            rh = rng.next_int(3) + 2
            pygame.draw.ellipse(surface, _PATH_PEBBLE, (px, py, rw, rh))
            pygame.draw.ellipse(
                surface, _PATH_PEBBLE_LIGHT, (px, py, rw - 1, rh - 1), 1
            )
        return surface

    def _make_tarmac(self, size: int) -> pygame.Surface:
        surface = pygame.Surface((size, size))
        surface.fill(_TARMAC_BASE)
        rng = _SeededRng(13)
        for _ in range(10):
            px = rng.next_int(size)
            py = rng.next_int(size)
            pygame.draw.circle(surface, _TARMAC_MARK, (px, py), rng.next_int(4) + 2)
        return surface

    def _make_end(self, size: int) -> pygame.Surface:
        """Damier noir et blanc pour symboliser l'arrivée"""
        surface = pygame.Surface((size, size))
        tile = max(size // 4, 4)
        for row in range(size // tile + 1):
            for col in range(size // tile + 1):
                color = s.Color.WHITE if (row + col) % 2 == 0 else s.Color.BLACK
                pygame.draw.rect(surface, color, (col * tile, row * tile, tile, tile))
        return surface

    def _make_portal(self, size: int) -> pygame.Surface:
        """Portail elliptique violet avec halo"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2
        pygame.draw.ellipse(surface, (*_PORTAL_OUTER, 80), (cx - 22, cy - 26, 44, 52))
        pygame.draw.ellipse(surface, _PORTAL_OUTER, (cx - 16, cy - 20, 32, 40))
        pygame.draw.ellipse(surface, _PORTAL_INNER, (cx - 10, cy - 14, 20, 28))
        pygame.draw.ellipse(surface, _PORTAL_GLOW, (cx - 4, cy - 6, 8, 12))
        pygame.draw.ellipse(surface, _PORTAL_GLOW, (cx - 16, cy - 20, 32, 40), 2)
        return surface

    def draw(
        self,
        screen: pygame.Surface,
        grid: Grid,
        hovered_cell: Cell | None,
        selected_cell: Cell | None,
        start_cells: list[Cell],
        end_cells: list[Cell],
    ) -> None:
        """Dessine toutes les cases de la grille"""
        for row in grid.cells:
            for cell in row:
                self._draw_cell(
                    screen, cell, hovered_cell, selected_cell, start_cells, end_cells
                )
        self._draw_grid_lines(screen, grid)

    def _draw_cell(
        self,
        screen: pygame.Surface,
        cell: Cell,
        hovered_cell: Cell | None,
        selected_cell: Cell | None,
        start_cells: list[Cell],
        end_cells: list[Cell],
    ) -> None:
        rect = pygame.Rect(cell.pixel_x, cell.pixel_y, s.CELL_SIZE, s.CELL_SIZE)
        if cell in end_cells:
            screen.blit(self._end_surface, rect)
        elif cell in start_cells:
            screen.blit(self._path_surface, rect)
            screen.blit(self._portal_surface, rect)
        elif cell.cell_type == CellType.GRASS:
            screen.blit(self._grass_surface, rect)
        elif cell.cell_type == CellType.PATH:
            screen.blit(self._path_surface, rect)
        elif cell.cell_type == CellType.TOWER:
            screen.blit(self._tarmac_surface, rect)
        else:
            pygame.draw.rect(screen, s.Color.BLACK, rect)

        if selected_cell is not None and cell == selected_cell:
            pygame.draw.rect(screen, s.Color.CELL_SELECT, rect, 3)
        elif hovered_cell is not None and cell == hovered_cell:
            pygame.draw.rect(screen, s.Color.CELL_HOVER, rect, 2)

    def _draw_grid_lines(self, screen: pygame.Surface, grid: Grid):
        """Dessine les lignes de la grille par-dessus les cases"""
        for row in range(grid.rows + 1):
            pygame.draw.line(
                screen,
                s.Color.GRID_LINE,
                (0, row * s.CELL_SIZE),
                (grid.cols * s.CELL_SIZE, row * s.CELL_SIZE),
            )
        for col in range(grid.cols + 1):
            pygame.draw.line(
                screen,
                s.Color.GRID_LINE,
                (col * s.CELL_SIZE, 0),
                (col * s.CELL_SIZE, grid.rows * s.CELL_SIZE),
            )


class _SeededRng:
    """Générateur pseudo-aléatoire déterministe pour des textures reproductibles et visuellement aléatoires"""

    def __init__(self, seed: int):
        self._state = seed

    def next_int(self, bound: int) -> int:
        self._state = (self._state * 1664525 + 1013904223) & 0xFFFFFFFF
        return self._state % bound
