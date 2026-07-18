import pygame
from model.game_state import GameState
from model.grid import Grid
from model.cell import Cell, CellType
from model.merge_manager import MergeManager
from model.units.archer import Archer
from controller.wave_controller import WaveController
import settings as s
from model.boosters.booster_gold import BoosterGold
from model.boosters.booster_attack import BoosterAttack
from model.boosters.booster_range import BoosterRange
from model.boosters.booster_speed import BoosterSpeed
from model.boosters.booster_speed import Booster
from view.hud_view import HudView
from controller.sound_manager import SoundManager


class GameController:
    def __init__(
        self,
        game_state: GameState,
        grid: Grid,
        wave_controller: WaveController,
        wave_button_rect: pygame.Rect,
        menu_button_rect: pygame.Rect,
        info_button_rect: pygame.Rect,
        hud_view: HudView,
        sound_manager: SoundManager,
    ):
        self.game_state = game_state
        self.grid = grid
        self.wave_controller = wave_controller
        self.merge_manager = MergeManager()
        self.next_wave_button_rect = wave_button_rect
        self.menu_button_rect = menu_button_rect
        self.info_button_rect = info_button_rect
        self.hud_view = hud_view
        self.sound_manager = sound_manager
        self.selected_cell = None
        self.hovered_cell = None
        self.selected_unit_type = Archer
        self.projectiles = []

    def handle_event(self, event: pygame.event.Event) -> None:
        """Fonction qui récupère l'évènement et le délègue à la fonction adaptée"""
        if event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._handle_left_click(event.pos)
            elif event.button == 3:
                self._handle_right_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            self._handle_keydown(event.key)

    def _handle_mouse_motion(self, pos: tuple[int, int]) -> None:
        """Met à jour la case survolée"""
        x, y = pos
        if y < s.GRID_HEIGHT:
            self.hovered_cell = self.grid.get_cell_at_pixel(x, y)
        else:
            self.hovered_cell = None

    def _handle_left_click(self, pos: tuple[int, int]) -> None:
        """Gère le clic gauche sur la grille, délègue si c'est sur le HUD.
        On gère la sélection des cases, possibles que sur les cases TOWER.
        Si aucune case n'est sélectionnée, on sélectionne la case si elle est TOWER
        Si une case est déjà selectionnée,
        - si la case selectionnée est la meme que l'ancienne, on désélectionne
        - si c'est une autre case avec une unité, on tente une fusion
        - si c'est une autre case vide on tente un déplacement"""
        x, y = pos

        if y >= s.GRID_HEIGHT:
            self._handle_hud_click(x, y)
            return

        clicked_cell = self.grid.get_cell_at_pixel(x, y)
        if clicked_cell is None:
            return

        if self.selected_cell is None:
            if clicked_cell.unit is not None:
                self.selected_cell = clicked_cell
        elif clicked_cell == self.selected_cell:
            self.selected_cell = None
        elif clicked_cell.unit is not None:
            self._try_merge(self.selected_cell, clicked_cell)
            self.selected_cell = None
        else:
            self._try_move(self.selected_cell, clicked_cell)
            self.selected_cell = None

    def _handle_right_click(self, pos: tuple[int, int]) -> None:
        """Gère le clic droit : achète et place une unité sur la case ciblée si une case est ciblée
        Délègue si c'est sur le HUD"""
        x, y = pos
        if y >= s.GRID_HEIGHT:
            return
        cell = self.grid.get_cell_at_pixel(x, y)
        if cell is not None:
            self._try_place_unit(cell)

    def _handle_keydown(self, key: int) -> None:
        """Raccourcis clavier : ECHAP pour quitter ou ouvrir le menu et ESPACE pour accélérer la prochaine vague"""
        if key == pygame.K_ESCAPE:
            if self.game_state.playing or self.game_state.menu:
                self.game_state.toggle_menu()
                return
        if self.game_state.menu:
            return
        if key == pygame.K_SPACE:
            if self.wave_controller.is_between_waves:
                self.wave_controller.start_next_wave()

    def _handle_hud_click(self, x: int, y: int) -> None:
        """Gère les clics dans le bandeau HUD"""
        if self.menu_button_rect.collidepoint(x, y):
            self.game_state.toggle_menu()
            return
        if self.next_wave_button_rect.collidepoint(x, y):
            if self.wave_controller.is_between_waves:
                self.wave_controller.start_next_wave()
            return
        if self.hud_view.get_speed_button_clicked((x, y)):
            self.game_state.change_speed()
            return
        unit_type = self.hud_view.get_unit_button_clicked((x, y))
        if unit_type is not None:
            self.selected_unit_type = unit_type
            return
        booster_indice = self.hud_view.get_booster_clicked((x, y))
        if booster_indice is not None:
            self._activate_booster(booster_indice)

    def _activate_booster(self, booster_indice: int) -> None:
        """Active un booster et applique son effet immédiatement"""
        booster = self.game_state.get_booster(booster_indice)
        if not booster.available:
            return
        booster.activate()
        match booster:
            case BoosterGold():
                amount = 50 * max(self.game_state.wave, 1)
                self.game_state.add_gold(amount)
            case BoosterRange():
                for row in self.grid.cells:
                    for cell in row:
                        if cell.unit is not None:
                            cell.unit.range += 1.0
            case BoosterAttack():
                for row in self.grid.cells:
                    for cell in row:
                        if cell.unit is not None:
                            cell.unit.damage = int(cell.unit.damage * 1.2)
            case BoosterSpeed():
                for row in self.grid.cells:
                    for cell in row:
                        if cell.unit is not None:
                            cell.unit.attack_speed *= 1.2

    def _desactivate_booster(self, booster: Booster) -> None:
        """Retire l'effet d'un booster de vague sur toutes les unités"""
        if not booster.active:
            return
        booster.desactivate()

        match booster:
            case BoosterRange():
                for row in self.grid.cells:
                    for cell in row:
                        if cell.unit is not None:
                            cell.unit.range -= 1.0
            case BoosterAttack():
                for row in self.grid.cells:
                    for cell in row:
                        if cell.unit is not None:
                            cell.unit.damage = int(cell.unit.damage / 1.2)
            case BoosterSpeed():
                for row in self.grid.cells:
                    for cell in row:
                        if cell.unit is not None:
                            cell.unit.attack_speed /= 1.2

    def _try_place_unit(self, cell: Cell) -> None:
        """Achète et place une unité si la case est libre et l'or suffisant"""
        if not cell.unit_placeable:
            return
        if not self.game_state.spend_gold(self.game_state.unit_cost):
            return
        cell.unit = self.selected_unit_type()
        self.game_state.increment_unit_cost()
        self.sound_manager.play_place_unit()

    def _try_merge(self, cell1: Cell, cell2: Cell) -> None:
        """Fusionne les unités de deux cases si possible. L'unité résultante reste en cell2"""
        if cell1.unit is None or cell2.unit is None:
            return
        if not self.merge_manager.can_merge(cell1.unit, cell2.unit):
            return
        self.merge_manager.merge(cell2.unit, cell1.unit)
        cell1.unit = None
        self.sound_manager.play_place_unit()

    def _try_move(self, source: Cell, target: Cell) -> None:
        """Déplace une unité si des déplacements restants sont disponibles"""
        if source.unit is None:
            return
        if target.cell_type != CellType.TOWER or target.unit is not None:
            return
        if not self.game_state.use_move():
            return
        target.unit = source.unit
        source.unit = None

    def update(self, dt: float) -> None:
        """Met à jour les unités, les projectiles et les combats à chaque frame"""
        if not self.game_state.playing:
            return

        was_between = self.wave_controller.is_between_waves
        self.wave_controller.update(dt)
        is_between_now = self.wave_controller.is_between_waves

        if not was_between and is_between_now:  # La vague vient de se terminer
            for booster in self.game_state.boosters:
                if booster.active:
                    self._desactivate_booster(booster)

        for row in self.grid.cells:
            for cell in row:
                if cell.unit is not None:
                    targets = self._get_targets_in_range(cell)
                    spawn_x = cell.pixel_x + s.CELL_SIZE // 2
                    spawn_y = cell.pixel_y + s.CELL_SIZE // 2
                    new_projectiles = cell.unit.update(dt, targets, spawn_x, spawn_y)
                    self.projectiles.extend(new_projectiles)

        for projectile in self.projectiles:
            path = self.wave_controller.paths[projectile.target.path_index]
            projectile.update(dt, path)

        for projectile in self.projectiles:
            if not projectile.active:
                target = projectile.target
                if not target.alive:
                    self.game_state.add_gold(target.reward)
                    self.game_state.add_score(target.reward)

        self.projectiles = [p for p in self.projectiles if p.active]
        if self.wave_controller.current_wave is not None:
            self.wave_controller.current_wave.remove_dead()

    def _get_targets_in_range(self, cell: Cell) -> list:
        """Retourne les monstres actifs à portée de l'unité sur cette case"""
        unit = cell.unit
        targets = []
        for monster in self.wave_controller.get_active_monsters():
            if monster.alive:
                monster_cell = self._get_monster_cell(monster)
                if monster_cell is not None:
                    dist = abs(monster_cell.row - cell.row) + abs(
                        monster_cell.col - cell.col
                    )
                    if dist <= unit.range:
                        targets.append(monster)
        return targets

    def _get_monster_cell(self, monster) -> Cell | None:
        """Retourne la case sur laquelle se trouve un monstre selon sa progression"""
        path = self.wave_controller.paths[monster.path_index]
        index = min(int(monster.progress), len(path) - 1)
        return path[index]
