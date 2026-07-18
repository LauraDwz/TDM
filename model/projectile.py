from math import hypot
from model.monsters.monster import Monster
import settings as s


class Projectile:
    def __init__(self, x: float, y: float, target: Monster, damage: int, color: tuple):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.color = color
        self.active = True

    def update(self, dt: float, path: list) -> None:
        """Déplace le projectile vers la position actuelle de la cible"""
        if not self.target.alive:
            self.active = False
            return

        target_x, target_y = self._get_target_pixel(path)
        dx = target_x - self.x
        dy = target_y - self.y
        distance = hypot(dx, dy)

        if distance <= s.PROJECTILE_SPEED * dt:
            self.x = target_x
            self.y = target_y
            self._hit()
            return

        ratio = s.PROJECTILE_SPEED * dt / distance
        self.x += dx * ratio
        self.y += dy * ratio

    def _get_target_pixel(self, path: list) -> tuple[float, float]:
        """Retourne la position en pixels du monstre cible"""
        index = int(self.target.progress)
        if index >= len(path) - 1:
            cell = path[-1]
            return cell.pixel_x + s.CELL_SIZE // 2, cell.pixel_y + s.CELL_SIZE // 2

        current_cell = path[index]
        next_cell = path[index + 1]
        frac = self.target.progress - index

        x = (
            current_cell.pixel_x
            + (next_cell.pixel_x - current_cell.pixel_x) * frac
            + s.CELL_SIZE // 2
        )
        y = (
            current_cell.pixel_y
            + (next_cell.pixel_y - current_cell.pixel_y) * frac
            + s.CELL_SIZE // 2
        )
        return x, y

    def _hit(self) -> None:
        """Inflige les dégâts à la cible et désactive le projectile"""
        self.target.take_damage(self.damage)
        self.active = False

    def __repr__(self) -> str:
        return f"Projectile(pos=({self.x:.0f},{self.y:.0f}), target={self.target})"
