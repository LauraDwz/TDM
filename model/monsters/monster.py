from abc import ABC


class Monster(ABC):
    def __init__(
        self,
        base_hp: int,
        base_speed: float,
        base_reward: int,
        name: str,
        path_index: int,
    ):
        self.hp = base_hp
        self.max_hp = base_hp
        self.speed = base_speed
        self.reward = base_reward
        self.progress = 0.0
        self.alive = True
        self.path_index = path_index
        self.name = name

    def take_damage(self, amount: int) -> None:
        """Subit des dégâts. Marque le monstre comme mort si hp tombe à 0."""
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

    def move(self, dt: float) -> None:
        """Avance le monstre sur le chemin selon sa vitesse et le delta-time."""
        self.progress += self.speed * dt

    @property
    def hp_ratio(self) -> float:
        """Ratio PV restants / PV max, utile pour afficher la barre de pv."""
        return self.hp / self.max_hp

    def __repr__(self) -> str:
        return f"{self.name}(hp={self.hp}/{self.max_hp}, progress={self.progress:.1f})"
