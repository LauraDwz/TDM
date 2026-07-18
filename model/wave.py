from collections import deque
from model.monsters.monster import Monster


class Wave:
    def __init__(self, monsters: list[Monster], spawn_interval: float = 1.5):
        """Une wave a des monstres stockées dans une liste ordonnée à faire spawner
        Et un intervalle de temps en secondes entre chaque spawn
        La liste active représente les monstres actuellement sur le terrain"""
        self._queue = deque(monsters)
        self.active = []
        self.spawn_interval = spawn_interval
        self._spawn_timer = 0.0

    def update(self, dt: float) -> None:
        """Fait avancer le timer de spawn et libère un monstre si besoin"""
        if self._queue:
            self._spawn_timer += dt
            if self._spawn_timer >= self.spawn_interval:
                self._spawn_timer = 0.0
                self.active.append(self._queue.popleft())

    def remove_dead(self) -> None:
        """Retire de la liste active les monstres morts ou arrivés au bout"""
        self.active = [m for m in self.active if m.alive]

    @property
    def is_finished(self) -> bool:
        """La vague est terminée quand il n'y a plus rien en attente ni sur le terrain"""
        return not self._queue and not self.active

    def __repr__(self) -> str:
        return (
            f"Wave(en attente={len(self._queue)}, "
            f"actifs={len(self.active)}, "
            f"terminée={self.is_finished})"
        )
