from random import randint
from model.wave import Wave
from model.game_state import GameState
from model.monsters.goblin import Goblin
from model.monsters.orc import Orc

_MONSTER_MAP = {
    "G": Goblin,
    "O": Orc,
}

AUTO_WAVE_DELAY = 5.0


class WaveController:
    def __init__(
        self,
        game_state: GameState,
        paths: list[list],
        wave_definitions: list[dict],
        sound_manager=None,
    ):
        self.game_state = game_state
        self.paths = paths
        self._wave_definitions = wave_definitions
        self.sound_manager = sound_manager
        self.current_wave = None
        self._wave_index = 0
        self._between_waves = True
        self._auto_timer = AUTO_WAVE_DELAY

    def start_next_wave(self) -> None:
        """Lance la prochaine vague si disponible"""
        if self._wave_index >= len(self._wave_definitions):
            return

        definition = self._wave_definitions[self._wave_index]
        monsters = self._build_monsters(definition)
        self.current_wave = Wave(monsters, spawn_interval=definition["spawn_interval"])
        self._wave_index += 1
        self._between_waves = False
        self._auto_timer = AUTO_WAVE_DELAY
        self.game_state.next_wave()

    def _build_monsters(self, definition: dict) -> list:
        """Construit la liste de monstres depuis la définition JSON level. Si un seul chemin, path_index toujours 0 sinon le path_index vient du JSON"""
        monsters = []
        single_path = len(self.paths) == 1

        for entry in definition["monsters"]:
            cls = _MONSTER_MAP[entry["type"]]
            if single_path:
                path_index = 0
            else:
                path_index = entry.get("path", 0)
            monsters.append(cls(path_index=path_index))
        return monsters

    def update(self, dt: float) -> None:
        if self._between_waves:
            if self.has_more_waves:
                self._auto_timer -= dt
                if self._auto_timer <= 0:
                    self.start_next_wave()
            elif self.current_wave is not None and self.current_wave.is_finished:
                self.game_state.set_victory()
            return

        if self.current_wave is None:
            return
        count_before = len(self.current_wave.active)
        self.current_wave.update(dt)
        count_after = len(self.current_wave.active)
        if count_after > count_before:
            self.sound_manager.play_monster_spawn()
        self._move_monsters(dt)
        self._check_reached_end()
        self.current_wave.remove_dead()
        if self.current_wave.is_finished:
            self._between_waves = True

    def _move_monsters(self, dt: float) -> None:
        for monster in self.current_wave.active:
            monster.move(dt)

    def _check_reached_end(self) -> None:
        for monster in self.current_wave.active:
            path = self.paths[monster.path_index]
            if monster.progress >= len(path) - 1:
                monster.alive = False
                self.game_state.lose_life()

    def get_active_monsters(self) -> list:
        if self.current_wave is None:
            return []
        return self.current_wave.active

    @property
    def is_between_waves(self) -> bool:
        return self._between_waves

    @property
    def has_more_waves(self) -> bool:
        return self._wave_index < len(self._wave_definitions)

    @property
    def auto_timer(self) -> float:
        """Temps restant avant le spawn automatique, pour affichage dans le HUD"""
        return max(0.0, self._auto_timer)
