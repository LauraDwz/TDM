from abc import ABC
from model.projectile import Projectile


class Unit(ABC):
    def __init__(
        self,
        level: int,
        damage: int,
        atk_range: float,
        attack_speed: float,
        name: str,
        color: tuple,
    ):
        self.level = level
        self.damage = damage * (2 ** (level - 1))
        self.range = atk_range * (1.5 ** (level - 1))
        self.attack_speed = attack_speed * (2 ** (level - 1))
        self.name = name
        self.projectile_color = color
        self._attack_cooldown = 0.0

    def level_up(self) -> None:
        """Appelée lors d'une fusion d'unités. Augmente le niveau et recalcule les stats.
        Dégats et vitesse d'attaque x2, Range x1.5 à chaque gain de niveau"""
        self.level += 1
        self.damage *= 2
        self.attack_speed *= 1.5
        self.range *= 1.5

    def update(self, dt: float, targets: list, spawn_x: float, spawn_y: float) -> list:
        """Appelée à chaque frame par le controller.
        Retourne une liste de Projectile à ajouter au jeu."""
        self._attack_cooldown -= dt
        projectiles = []
        if self._attack_cooldown <= 0.0 and targets:
            target = targets[0]
            projectiles.append(
                Projectile(spawn_x, spawn_y, target, self.damage, self.projectile_color)
            )
            self._attack_cooldown = 1.0 / self.attack_speed
        return projectiles

    def __repr__(self) -> str:
        return (
            f"{self.name()}(level={self.level}, dmg={self.damage}, "
            f"range={self.range:.1f}, spd={self.attack_speed:.1f})"
        )
