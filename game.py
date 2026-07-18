import pygame
import settings as s
from model.app_status import AppStatus
from model.game_state import GameState
from model.grid import Grid
from controller.path_finder import PathFinder
from controller.wave_controller import WaveController
from controller.game_controller import GameController
from view.grid_view import GridView
from view.unit_view import UnitView
from view.hud_view import HudView
from view.menu_view import MenuView
from view.map_view import MapView
from view.end_screen_view import EndScreenView
from view.wave_info_view import WaveInfoView
from view.scoreboard_view import ScoreboardView
from data.level_loader import get_level, load_levels
from data.scoreboard import add_score
from controller.sound_manager import SoundManager


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))
        pygame.display.set_caption(s.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.app_status = AppStatus.MAP
        self._current_level_index = None
        self._total_levels = len(load_levels())
        self._show_wave_info = False

        self.map_view = MapView()
        self.menu_view = MenuView()
        self.end_screen_view = EndScreenView()
        self.wave_info_view = WaveInfoView()
        self.scoreboard_view = ScoreboardView()
        self._show_scoreboard = False
        self._scoreboard_level = None
        self.sound_manager = SoundManager()
        self.sound_manager.play_map_music()

        self.game_state = None
        self.grid = None
        self.paths = None
        self.start_cells = None
        self.end_cells = None
        self.wave_controller = None
        self.game_controller = None
        self.grid_view = None
        self.unit_view = None
        self.hud_view = None

    def _load_level(self, level_index: int):
        self._current_level_index = level_index
        self._show_wave_info = False
        level_data = get_level(level_index)

        self.game_state = GameState()
        self.grid = Grid(level_data["layout"])

        path_finder = PathFinder()
        raw_starts = (
            level_data["starts"] if "starts" in level_data else [level_data["start"]]
        )
        raw_ends = level_data["ends"] if "ends" in level_data else [level_data["end"]]
        self.start_cells = [self.grid.get_cell(r, c) for r, c in raw_starts]
        self.end_cells = [self.grid.get_cell(r, c) for r, c in raw_ends]
        self.paths = path_finder.calculate_paths(
            self.grid, self.start_cells, self.end_cells
        )

        self.grid_view = GridView()
        self.unit_view = UnitView()
        self.hud_view = HudView()

        self.wave_controller = WaveController(
            self.game_state, self.paths, level_data["waves"], self.sound_manager
        )
        self.game_controller = GameController(
            self.game_state,
            self.grid,
            self.wave_controller,
            self.hud_view.wave_button_rect,
            self.hud_view.pause_button_rect,
            self.hud_view.info_button_rect,
            self.hud_view,
            self.sound_manager,
        )
        self.app_status = AppStatus.PLAYING
        self._show_wave_info = False
        self._show_scoreboard = False
        self.sound_manager.play_game_music()

    def _return_to_map(self):
        self.app_status = AppStatus.MAP
        self._show_wave_info = False
        self.map_view._show_rules = False
        self.sound_manager.play_map_music()
        self.game_state = None
        self.grid = None
        self.paths = None
        self.start_cells = None
        self.end_cells = None
        self.wave_controller = None
        self.game_controller = None
        self.grid_view = None
        self.unit_view = None
        self.hud_view = None

    @property
    def _has_next_level(self) -> bool:
        return (
            self._current_level_index is not None
            and self._current_level_index + 1 < self._total_levels
        )

    def run(self):
        while self.running:
            dt = self.clock.tick(s.FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if self.app_status == AppStatus.MAP:
                self._handle_map_events(event)
            elif self.app_status == AppStatus.PLAYING:
                self._handle_game_events(event)

    def _handle_map_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.map_view.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._show_scoreboard:
                if self.scoreboard_view.handle_click(
                    event.pos, self._total_levels, None
                ):
                    self._show_scoreboard = False
                return
            result = self.map_view.handle_click(event.pos)
            if result == "scores":
                self._show_scoreboard = True
                self._scoreboard_level = None
                self.scoreboard_view.reset()
            elif result is not None:
                self.map_view._show_rules = False
                self._load_level(result)

    def _handle_game_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._show_wave_info:
                if self.wave_info_view.handle_click(event.pos):
                    self._show_wave_info = False
                    if self.game_state.info:
                        self.game_state.toggle_info()
                return

            # Bouton info
            if self.hud_view.is_info_button_clicked(event.pos):
                if not self._show_wave_info:
                    self._show_wave_info = True
                    if self.game_state.playing:
                        self.game_state.toggle_info()
                return

            # Scoreboard ouvert
            if self._show_scoreboard:
                if self.scoreboard_view.handle_click(
                    event.pos, self._total_levels, self._scoreboard_level
                ):
                    self._show_scoreboard = False
                return

            # Ecrans de fin
            if self.game_state.victory:
                action = self.end_screen_view.handle_click_victory(
                    event.pos, self._has_next_level
                )
                if action == "next":
                    self._load_level(self._current_level_index + 1)
                elif action == "scores":
                    self._show_scoreboard = True
                    self._scoreboard_level = self._current_level_index
                    self.scoreboard_view.reset()
                elif action == "map":
                    self._return_to_map()
                return

            if self.game_state.game_over:
                action = self.end_screen_view.handle_click_defeat(event.pos)
                if action == "restart":
                    self._load_level(self._current_level_index)
                elif action == "map":
                    self._return_to_map()
                return

            # Menu pause
            if self.game_state.menu:
                action = self.menu_view.handle_click(event.pos)
                if action == "resume":
                    self.game_state.toggle_menu()
                    self.menu_view.reset()
                elif action == "restart":
                    self.menu_view.reset()
                    self._load_level(self._current_level_index)
                elif action == "map":
                    self.menu_view.reset()
                    self._return_to_map()
                elif action == "mute_music":
                    self.sound_manager.toggle_music()
                elif action == "mute_sfx":
                    self.sound_manager.toggle_sfx()
                elif action == "quit":
                    self.running = False
                return

        if not self.game_state.victory and not self.game_state.game_over:
            self.game_controller.handle_event(event)

    def _update(self, dt: float):
        if self.app_status == AppStatus.PLAYING:
            if self.game_state.playing:
                self.game_state.elapsed_time += dt
            was_victory = self.game_state.victory
            scaled_dt = dt * self.game_state.speed.get_speed()
            self.game_controller.update(scaled_dt)
            if not was_victory and self.game_state.victory:
                add_score(
                    self._current_level_index,
                    self.game_state.score,
                    self.game_state.elapsed_time,
                    self.game_state.lives,
                )

    def _draw(self):
        if self.app_status == AppStatus.MAP:
            self.map_view.draw(self.screen)
            if self._show_scoreboard:
                self.scoreboard_view.draw(self.screen, self._total_levels, None)
        elif self.app_status == AppStatus.PLAYING:
            self._draw_game()
        pygame.display.flip()

    def _draw_game(self):
        self.screen.fill(s.Color.BACKGROUND)
        self.grid_view.draw(
            self.screen,
            self.grid,
            self.game_controller.hovered_cell,
            self.game_controller.selected_cell,
            self.start_cells,
            self.end_cells,
        )
        self.unit_view.draw(
            self.screen,
            self.grid,
            self.wave_controller.get_active_monsters(),
            self.paths,
            self.game_controller.projectiles,
        )
        self.hud_view.draw(
            self.screen,
            self.game_state,
            self.game_controller.selected_unit_type,
            self.wave_controller.is_between_waves,
            self.wave_controller.has_more_waves,
            self.wave_controller.auto_timer,
        )
        if self._show_scoreboard:
            self.scoreboard_view.draw(
                self.screen, self._total_levels, self._scoreboard_level
            )
        elif self._show_wave_info:
            self.wave_info_view.draw(
                self.screen,
                self.wave_controller._wave_definitions,
                self.wave_controller._wave_index,
            )
        elif self.game_state.menu:
            self.menu_view.draw(self.screen, self.sound_manager)
        elif self.game_state.victory:
            self.end_screen_view.draw_victory(
                self.screen, self.game_state, self._has_next_level
            )
        elif self.game_state.game_over:
            self.end_screen_view.draw_defeat(self.screen)
