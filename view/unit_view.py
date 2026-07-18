import pygame
from model.grid import Grid
from model.cell import Cell
from model.monsters.monster import Monster
from model.monsters.goblin import Goblin
from model.monsters.orc import Orc
from model.units.archer import Archer
from model.units.mage import Mage
import settings as s

_GOBLIN_BODY = (60, 160, 60)
_GOBLIN_DARK = (30, 110, 30)
_GOBLIN_EYE = (255, 255, 80)
_GOBLIN_PUPIL = (20, 20, 20)
_GOBLIN_MOUTH = (20, 80, 20)
_GOBLIN_EAR = (40, 130, 40)

_ORC_BODY = (200, 50, 50)
_ORC_DARK = (140, 20, 20)
_ORC_EYE = (255, 200, 0)
_ORC_PUPIL = (20, 20, 20)
_ORC_TUSK = (240, 220, 180)
_ORC_HORN = (80, 40, 20)


class UnitView:
    def __init__(self):
        self._font_level = pygame.font.SysFont(None, 22)

    def draw(
        self,
        screen: pygame.Surface,
        grid: Grid,
        monsters: list[Monster],
        paths: list[list[Cell]],
        projectiles: list,
    ):
        """Dessine toutes les unités, les monstres puis les projectiles"""
        self._draw_units(screen, grid)
        self._draw_monsters(screen, monsters, paths)
        self._draw_projectiles(screen, projectiles)

    def _draw_units(self, screen: pygame.Surface, grid: Grid):
        for row in grid.cells:
            for cell in row:
                if cell.unit is not None:
                    self._draw_unit(screen, cell)

    def _draw_unit(self, screen: pygame.Surface, cell: Cell) -> None:
        unit = cell.unit
        color = self._get_unit_color(unit)
        center_x = cell.pixel_x + s.CELL_SIZE // 2
        center_y = cell.pixel_y + s.CELL_SIZE // 2
        radius = s.CELL_SIZE // 2 - 6
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
        self._draw_level(screen, unit.level, center_x, center_y)

    def _get_unit_color(self, unit) -> tuple:
        if isinstance(unit, Archer):
            return s.Color.UNIT_ARCHER
        if isinstance(unit, Mage):
            return s.Color.UNIT_MAGE
        return s.Color.WHITE

    def _draw_level(self, screen: pygame.Surface, level: int, x: int, y: int) -> None:
        text = self._font_level.render(str(level), True, s.Color.WHITE)
        rect = text.get_rect(center=(x, y))
        screen.blit(text, rect)

    def _draw_monsters(
        self, screen: pygame.Surface, monsters: list[Monster], paths: list[list[Cell]]
    ):
        for monster in monsters:
            if monster.alive:
                path = paths[monster.path_index]
                self._draw_monster(screen, monster, path)

    def _draw_monster(self, screen: pygame.Surface, monster: Monster, path: list[Cell]):
        index = int(monster.progress)
        if index >= len(path) - 1:
            return

        current_cell = path[index]
        next_cell = path[index + 1]
        frac = monster.progress - index

        cx = int(
            current_cell.pixel_x
            + (next_cell.pixel_x - current_cell.pixel_x) * frac
            + s.CELL_SIZE // 2
        )
        cy = int(
            current_cell.pixel_y
            + (next_cell.pixel_y - current_cell.pixel_y) * frac
            + s.CELL_SIZE // 2
        )

        if isinstance(monster, Goblin):
            self._draw_goblin(screen, cx, cy)
        elif isinstance(monster, Orc):
            self._draw_orc(screen, cx, cy)
        else:
            pygame.draw.circle(
                screen, s.Color.MONSTER_BASE, (cx, cy), s.CELL_SIZE // 2 - 8
            )

        radius = s.CELL_SIZE // 2 - 8
        self._draw_health_bar(screen, monster, cx, cy, radius)

    def _draw_goblin(self, screen: pygame.Surface, cx: int, cy: int):
        """Goblin : petit, vert, grandes oreilles pointues et gros yeux"""
        r = 10

        for dx in (-r, r):
            ear_points = [
                (cx + dx, cy - r + 2),
                (cx + dx + (6 if dx > 0 else -6), cy - r - 8),
                (cx + dx + (3 if dx > 0 else -3), cy + 2),
            ]
            pygame.draw.polygon(screen, _GOBLIN_EAR, ear_points)

        pygame.draw.circle(screen, _GOBLIN_BODY, (cx, cy), r)
        pygame.draw.circle(screen, _GOBLIN_DARK, (cx, cy), r, 1)

        for ex, ey in [(cx - 4, cy - 2), (cx + 4, cy - 2)]:
            pygame.draw.circle(screen, _GOBLIN_EYE, (ex, ey), 3)
            pygame.draw.circle(screen, _GOBLIN_PUPIL, (ex, ey), 1)

        pygame.draw.arc(screen, _GOBLIN_MOUTH, (cx - 4, cy + 1, 8, 5), 3.9, 5.5, 2)

    def _draw_orc(self, screen: pygame.Surface, cx: int, cy: int) -> None:
        """Orc : imposant, rouge foncé, large crâne, cornes épaisses, défenses visibles"""
        r = 17

        for side in (-1, 1):
            base_x = cx + side * (r - 5)
            base_y = cy - r + 4
            tip_x = cx + side * (r + 4)
            tip_y = cy - r - 14
            mid_x = cx + side * (r + 1)
            mid_y = cy - r - 6
            horn_points = [
                (base_x - side * 4, base_y),
                (base_x + side * 3, base_y + 2),
                (mid_x + side * 2, mid_y),
                (tip_x, tip_y),
                (mid_x - side * 1, mid_y),
            ]
            pygame.draw.polygon(screen, _ORC_HORN, horn_points)
            pygame.draw.polygon(screen, _ORC_DARK, horn_points, 1)

        pygame.draw.circle(screen, _ORC_DARK, (cx + 2, cy + 2), r)
        pygame.draw.circle(screen, _ORC_BODY, (cx, cy), r)
        pygame.draw.circle(screen, (220, 80, 80), (cx - 5, cy - 5), r // 3)
        pygame.draw.circle(screen, _ORC_DARK, (cx, cy), r, 2)
        pygame.draw.line(screen, _ORC_DARK, (cx - 11, cy - 8), (cx - 4, cy - 5), 3)
        pygame.draw.line(screen, _ORC_DARK, (cx + 4, cy - 5), (cx + 11, cy - 8), 3)
        for ex, ey in [(cx - 6, cy - 3), (cx + 6, cy - 3)]:
            pygame.draw.circle(screen, _ORC_EYE, (ex, ey), 4)
            pygame.draw.circle(screen, _ORC_PUPIL, (ex, ey), 2)

        pygame.draw.ellipse(screen, _ORC_DARK, (cx - 4, cy + 1, 8, 5))
        for nx in (cx - 2, cx + 2):
            pygame.draw.circle(screen, (100, 10, 10), (nx, cy + 4), 1)

        pygame.draw.arc(screen, _ORC_DARK, (cx - 7, cy + 5, 14, 8), 3.4, 6.0, 2)

        for tx, flip in [(cx - 7, 0), (cx + 3, 1)]:
            tusk = [
                (tx, cy + r - 5),
                (tx + 4, cy + r - 5),
                (tx + 3 + flip, cy + r + 2),
                (tx + 1, cy + r + 2),
            ]
            pygame.draw.polygon(screen, _ORC_TUSK, tusk)
            pygame.draw.polygon(screen, (180, 160, 120), tusk, 1)

    def _draw_health_bar(
        self, screen: pygame.Surface, monster: Monster, cx: int, cy: int, radius: int
    ):
        bar_width = radius * 2
        bar_height = 4
        bar_x = cx - radius
        bar_y = cy - radius - 8

        pygame.draw.rect(
            screen, s.Color.HEALTH_BG, (bar_x, bar_y, bar_width, bar_height)
        )
        filled_width = int(bar_width * monster.hp_ratio)
        pygame.draw.rect(
            screen, s.Color.HEALTH_BAR, (bar_x, bar_y, filled_width, bar_height)
        )

    def _draw_projectiles(self, screen: pygame.Surface, projectiles: list):
        for projectile in projectiles:
            if projectile.active:
                pygame.draw.circle(
                    screen, projectile.color, (int(projectile.x), int(projectile.y)), 5
                )
