import pygame
from model.game_state import GameState
import settings as s
from model.units.archer import Archer
from model.units.mage import Mage

_HUD_MID = s.GRID_HEIGHT + s.HUD_HEIGHT // 2

_UNIT_BTN_W = 56
_UNIT_BTN_H = 56
_UNIT_BTN_Y = _HUD_MID - _UNIT_BTN_H // 2

_BOOST_BTN_W = 52
_BOOST_BTN_H = 26
_BOOST_GAP = 4
_BOOST_BLOCK_H = 14 + 4 + 2 * _BOOST_BTN_H + _BOOST_GAP
_BOOST_START_X = 630
_BOOST_START_Y = s.GRID_HEIGHT + (s.HUD_HEIGHT - _BOOST_BLOCK_H) // 2 + 14

_BOOSTER_NUMBER = 4


class HudView:
    def __init__(self):
        self.font_large = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 22)
        self.font_button = pygame.font.SysFont(None, 20)
        self.font_unit_key = pygame.font.SysFont(None, 32)
        self.font_cost = pygame.font.SysFont(None, 20)
        self.font_boost = pygame.font.SysFont(None, 17)
        self.font_info = pygame.font.SysFont(None, 36)

        self.archer_button_rect = pygame.Rect(
            450, _UNIT_BTN_Y, _UNIT_BTN_W, _UNIT_BTN_H
        )
        self.mage_button_rect = pygame.Rect(530, _UNIT_BTN_Y, _UNIT_BTN_W, _UNIT_BTN_H)
        self.speed_button_rect = pygame.Rect(370, _UNIT_BTN_Y, _UNIT_BTN_W, _UNIT_BTN_H)

        self.info_button_rect = pygame.Rect(142, _UNIT_BTN_Y, _UNIT_BTN_W, _UNIT_BTN_H)

        self.booster_rects = self._build_booster_rects()

        self.wave_button_rect = pygame.Rect(
            s.WINDOW_WIDTH - 230, s.GRID_HEIGHT + 68, 210, 44
        )
        self.pause_button_rect = pygame.Rect(
            s.WINDOW_WIDTH - 230, s.GRID_HEIGHT + 16, 210, 44
        )

    def _build_booster_rects(self) -> list:
        """Construit les rects des 4 boutons boosters en grille 2x2"""
        rects = []
        for i in range(_BOOSTER_NUMBER):
            col = i % 2
            row = i // 2
            x = _BOOST_START_X + col * (_BOOST_BTN_W + _BOOST_GAP)
            y = _BOOST_START_Y + row * (_BOOST_BTN_H + _BOOST_GAP)
            rects.append(pygame.Rect(x, y, _BOOST_BTN_W, _BOOST_BTN_H))
        return rects

    def draw(
        self,
        screen: pygame.Surface,
        game_state: GameState,
        selected_unit_type,
        is_between_waves: bool,
        has_more_waves: bool,
        auto_timer: float = 0,
    ) -> None:
        """Dessine le bandeau HUD en bas de la fenêtre"""
        self._draw_background(screen)
        self._draw_gold(screen, game_state.gold)
        self._draw_lives(screen, game_state.lives)
        self._draw_wave(screen, game_state.wave)
        self._draw_score(screen, game_state.score)
        self._draw_moves(screen, game_state.moves_remaining)
        self._draw_unit_buttons(
            screen, selected_unit_type, game_state.unit_cost, game_state.gold
        )
        self._draw_speed_button(screen, game_state.speed)
        self._draw_booster_buttons(screen, game_state)
        self._draw_info_button(screen)
        self._draw_wave_button(screen, is_between_waves, has_more_waves, auto_timer)
        self._draw_pause_button(screen)

    def _draw_background(self, screen: pygame.Surface) -> None:
        hud_rect = pygame.Rect(0, s.GRID_HEIGHT, s.WINDOW_WIDTH, s.HUD_HEIGHT)
        pygame.draw.rect(screen, s.Color.HUD_BG, hud_rect)
        pygame.draw.line(
            screen,
            s.Color.GRID_LINE,
            (0, s.GRID_HEIGHT),
            (s.WINDOW_WIDTH, s.GRID_HEIGHT),
            2,
        )

    def _draw_gold(self, screen: pygame.Surface, gold: int) -> None:
        text = self.font_large.render(f"Or : {gold}", True, s.Color.GOLD)
        rect = text.get_rect(midleft=(20, _HUD_MID - 18))
        screen.blit(text, rect)

    def _draw_lives(self, screen: pygame.Surface, lives: int) -> None:
        text = self.font_large.render(f"Vies : {lives}", True, s.Color.HEART)
        rect = text.get_rect(midleft=(20, _HUD_MID + 18))
        screen.blit(text, rect)

    def _draw_wave(self, screen: pygame.Surface, wave: int) -> None:
        text = self.font_small.render(f"Vague : {wave}", True, s.Color.HUD_TEXT)
        rect = text.get_rect(midleft=(220, _HUD_MID - 14))
        screen.blit(text, rect)

    def _draw_score(self, screen: pygame.Surface, score: int) -> None:
        text = self.font_small.render(f"Score : {score}", True, s.Color.HUD_TEXT)
        rect = text.get_rect(midleft=(220, _HUD_MID + 14))
        screen.blit(text, rect)

    def _draw_moves(self, screen: pygame.Surface, moves: int) -> None:
        color = s.Color.GOLD if moves > 0 else s.Color.HEART
        text = self.font_small.render(f"Déplacements : {moves}", True, color)
        rect = text.get_rect(midleft=(220, _HUD_MID + 36))
        screen.blit(text, rect)

    def _draw_unit_buttons(
        self, screen: pygame.Surface, selected_unit_type, unit_cost: int, gold: int
    ) -> None:
        can_afford = gold >= unit_cost
        self._draw_unit_button(
            screen,
            self.archer_button_rect,
            "A",
            s.Color.UNIT_ARCHER,
            selected_unit_type is Archer,
            unit_cost,
            can_afford,
        )
        self._draw_unit_button(
            screen,
            self.mage_button_rect,
            "M",
            s.Color.UNIT_MAGE,
            selected_unit_type is Mage,
            unit_cost,
            can_afford,
        )

    def _draw_unit_button(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        key: str,
        color: tuple,
        selected: bool,
        unit_cost: int,
        can_afford: bool = True,
    ) -> None:
        draw_color = color if can_afford else tuple(max(0, c - 80) for c in color)
        border_color = (
            s.Color.WHITE
            if selected
            else ((100, 100, 100) if can_afford else (60, 60, 60))
        )
        border_width = 3 if selected else 1
        pygame.draw.rect(screen, draw_color, rect, border_radius=8)
        pygame.draw.rect(screen, border_color, rect, border_width, border_radius=8)
        label_color = s.Color.WHITE if can_afford else (140, 140, 140)
        label = self.font_unit_key.render(key, True, label_color)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)
        cost_color = s.Color.GOLD if can_afford else (120, 100, 40)
        cost_text = self.font_cost.render(f"{unit_cost} or", True, cost_color)
        cost_rect = cost_text.get_rect(midtop=(rect.centerx, rect.bottom + 4))
        screen.blit(cost_text, cost_rect)

    def _draw_booster_buttons(
        self, screen: pygame.Surface, game_state: GameState
    ) -> None:
        """Dessine le titre 'Boost' et les 4 boutons boosters en grille 2x2"""
        title = self.font_boost.render("Boost", True, (200, 200, 200))
        title_rect = title.get_rect(
            midbottom=(
                _BOOST_START_X + _BOOST_BTN_W + _BOOST_GAP // 2,
                _BOOST_START_Y - 4,
            )
        )
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.booster_rects):
            booster = game_state.get_booster(i)
            self._draw_booster_button(screen, rect, booster, mouse_pos)

    def _draw_booster_button(self, screen, rect, booster, mouse_pos) -> None:
        base_color = booster.color
        if not booster.available:
            color = (50, 50, 50)
            border_color = (80, 80, 80)
            text_color = (100, 100, 100)
        elif rect.collidepoint(mouse_pos):
            color = tuple(min(255, c + 40) for c in base_color)
            border_color = s.Color.WHITE
            text_color = s.Color.WHITE
        else:
            color = base_color
            border_color = tuple(max(0, c - 40) for c in base_color)
            text_color = s.Color.WHITE

        pygame.draw.rect(screen, color, rect, border_radius=6)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=6)

        label = self.font_boost.render(booster.label, True, text_color)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

        if booster.active:
            active_text = self.font_boost.render("o", True, s.Color.GOLD)
            active_rect = active_text.get_rect(topright=(rect.right - 2, rect.top + 2))
            screen.blit(active_text, active_rect)

    def _draw_wave_button(
        self,
        screen: pygame.Surface,
        is_between_waves: bool,
        has_more_waves: bool,
        auto_timer: float = 0,
    ) -> None:
        if not is_between_waves or not has_more_waves:
            return
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.wave_button_rect.collidepoint(mouse_pos)
        color = s.Color.BUTTON_HOVER if hovered else s.Color.BUTTON
        pygame.draw.rect(screen, color, self.wave_button_rect, border_radius=8)
        label = self.font_button.render(
            f"Vague suivante ({int(auto_timer)+1}s)", True, s.Color.WHITE
        )
        rect = label.get_rect(center=self.wave_button_rect.center)
        screen.blit(label, rect)

    def _draw_pause_button(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.pause_button_rect.collidepoint(mouse_pos)
        color = s.Color.BUTTON_HOVER if hovered else s.Color.BUTTON
        pygame.draw.rect(screen, color, self.pause_button_rect, border_radius=6)
        label = self.font_button.render("Pause  [Echap]", True, s.Color.WHITE)
        rect = label.get_rect(center=self.pause_button_rect.center)
        screen.blit(label, rect)

    def _draw_speed_button(self, screen: pygame.Surface, speed) -> None:
        rect = self.speed_button_rect
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)
        bg_color = (80, 80, 80) if hovered else (50, 50, 50)
        pygame.draw.rect(screen, bg_color, rect, border_radius=8)
        pygame.draw.rect(screen, (120, 120, 120), rect, 1, border_radius=8)

        count = speed.triangle_count()
        triangle_w = 10
        triangle_h = 14
        gap = 4
        total_w = count * triangle_w + (count - 1) * gap
        start_x = rect.centerx - total_w // 2
        cy = rect.centery

        for i in range(count):
            tx = start_x + i * (triangle_w + gap)
            points = [
                (tx, cy - triangle_h // 2),
                (tx, cy + triangle_h // 2),
                (tx + triangle_w, cy),
            ]
            pygame.draw.polygon(screen, s.Color.WHITE, points)

        label = self.font_cost.render("vitesse", True, (160, 160, 160))
        label_rect = label.get_rect(midtop=(rect.centerx, rect.bottom + 4))
        screen.blit(label, label_rect)

    def is_wave_button_clicked(self, pos: tuple[int, int]) -> bool:
        return self.wave_button_rect.collidepoint(pos)

    def is_pause_button_clicked(self, pos: tuple[int, int]) -> bool:
        return self.pause_button_rect.collidepoint(pos)

    def get_speed_button_clicked(self, pos: tuple[int, int]) -> bool:
        return self.speed_button_rect.collidepoint(pos)

    def get_unit_button_clicked(self, pos: tuple[int, int]):
        if self.archer_button_rect.collidepoint(pos):
            return Archer
        if self.mage_button_rect.collidepoint(pos):
            return Mage
        return None

    def _draw_info_button(self, screen: pygame.Surface):
        rect = self.info_button_rect
        mouse_pos = pygame.mouse.get_pos()
        color = (60, 120, 220) if rect.collidepoint(mouse_pos) else (40, 90, 180)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (100, 160, 255), rect, 2, border_radius=8)
        label = self.font_info.render("i", True, s.Color.WHITE)
        screen.blit(label, label.get_rect(center=rect.center))

    def is_info_button_clicked(self, pos: tuple[int, int]) -> bool:
        return self.info_button_rect.collidepoint(pos)

    def get_booster_clicked(self, pos: tuple[int, int]):
        """Retourne l'indice du booster cliqué ou None"""
        for i, rect in enumerate(self.booster_rects):
            if rect.collidepoint(pos):
                return i
        return None
