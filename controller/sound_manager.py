import os
import pygame


def _path(filename: str) -> str:
    return "assets\\sounds\\" + filename


class SoundManager:
    def __init__(self):
        self.music_enabled = True
        self.sfx_enabled = True
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._current_music = None
        self._load_sounds()

    def _load_sounds(self) -> None:
        sfx_files = {
            "place_unit": "place_unit.mp3",
            "monster_spawn": "monster_spawn.mp3",
        }
        for key, filename in sfx_files.items():
            full_path = _path(filename)
            if os.path.exists(full_path):
                try:
                    self._sounds[key] = pygame.mixer.Sound(full_path)
                except Exception:
                    print("Soucis avec le son")

    def _play_music(self, filename: str) -> None:
        """Lance une musique en boucle. Ne recharge pas si déjà en cours"""
        if self._current_music == filename:
            return
        full_path = _path(filename)
        if not os.path.exists(full_path):
            return
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(0.5 if self.music_enabled else 0.0)
            pygame.mixer.music.play(-1)
            self._current_music = filename
        except Exception:
            print("Soucis avec la musique")

    def play_map_music(self) -> None:
        self._play_music("music_map.mp3")

    def play_game_music(self) -> None:
        self._play_music("music_game.mp3")

    def toggle_music(self) -> None:
        self.music_enabled = not self.music_enabled
        pygame.mixer.music.set_volume(0.5 if self.music_enabled else 0.0)

    def toggle_sfx(self) -> None:
        self.sfx_enabled = not self.sfx_enabled

    def play(self, key: str) -> None:
        if not self.sfx_enabled:
            return
        sound = self._sounds.get(key)
        if sound:
            sound.play()

    def play_place_unit(self) -> None:
        self.play("place_unit")

    def play_monster_spawn(self) -> None:
        self.play("monster_spawn")
