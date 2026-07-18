import pygame
import settings as s
from data.rules import RULES

TOTAL_LEVELS = 16
COLS = 4
NODE_RADIUS = 32
NODE_MARGIN_X = s.WINDOW_WIDTH // (COLS + 1)
NODE_SPACING_Y = 90

_TITLE_H = 80
_SERPENTIN_H = (TOTAL_LEVELS // COLS - 1) * NODE_SPACING_Y  # 3 intervalles = 270px
_BUTTON_H = 44
_HINT_H = 22
_GAP = 20

_TOTAL_CONTENT_H = _TITLE_H + _GAP + _SERPENTIN_H + _GAP + _BUTTON_H + _GAP + _HINT_H
_START_Y = (s.WINDOW_HEIGHT - _TOTAL_CONTENT_H) // 2

_SERPENTIN_TOP = _START_Y + _TITLE_H + _GAP + NODE_RADIUS - 10
_SERPENTIN_BOTTOM = _SERPENTIN_TOP + _SERPENTIN_H

_TITLE_Y = _SERPENTIN_TOP // 2
_SERPENTIN_Y = _SERPENTIN_TOP
_BUTTON_Y = (_SERPENTIN_BOTTOM + NODE_RADIUS + s.WINDOW_HEIGHT - 30) // 2 - 22
_HINT_Y = s.WINDOW_HEIGHT - 30


def _calculate_node_positions() -> list[tuple[int, int]]:
    """Calcule les positions (x, y) des 16 nœuds en serpentin vertical => ligne paire gauche vers droite et ligne impaire droite vers gauche"""
    positions = []
    for i in range(TOTAL_LEVELS):
        row = i // COLS
        col = i % COLS
        if row % 2 == 1:
            col = (COLS - 1) - col
        x = NODE_MARGIN_X + col * NODE_MARGIN_X
        y = _SERPENTIN_Y + row * NODE_SPACING_Y
        positions.append((x, y))
    return positions


NODE_POSITIONS = _calculate_node_positions()


class MapView:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 64)
        self.font_level = pygame.font.SysFont(None, 32)
        self.font_button = pygame.font.SysFont(None, 28)
        self.font_rules = pygame.font.SysFont(None, 24)
        self.font_hint = pygame.font.SysFont(None, 22)

        self._hovered_level = None
        self._show_rules = False

        button_w = 260
        button_h = 44
        self.rules_button_rect = pygame.Rect(
            s.WINDOW_WIDTH // 2 - button_w - 10, _BUTTON_Y, button_w, button_h
        )
        self.scores_button_rect = pygame.Rect(
            s.WINDOW_WIDTH // 2 + 10, _BUTTON_Y, button_w, button_h
        )
        self.back_rect = pygame.Rect(s.WINDOW_WIDTH // 2 - 160, 710, 320, 44)

    def handle_mouse_motion(self, pos: tuple[int, int]) -> None:
        """Met à jour le niveau survolé"""
        self._hovered_level = self._get_level_at(pos)

    def handle_click(self, pos: tuple[int, int]) -> int | None:
        """Gère un clic sur la carte. Retourne l'index du niveau cliqué, ou None"""
        if self._show_rules:
            if self.back_rect.collidepoint(pos):
                self._show_rules = False
            return None

        if self.rules_button_rect.collidepoint(pos):
            self._show_rules = True
            return None

        if self.scores_button_rect.collidepoint(pos):
            return "scores"

        return self._get_level_at(pos)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(s.Color.BLACK)
        if self._show_rules:
            self._draw_rules_screen(screen)
        else:
            self._draw_map(screen)

    def _draw_map(self, screen: pygame.Surface) -> None:
        self._draw_title(screen)
        self._draw_connections(screen)
        self._draw_nodes(screen)
        self._draw_rules_button(screen)
        self._draw_scores_button(screen)
        self._draw_hint(screen)

    def _draw_title(self, screen: pygame.Surface) -> None:
        text = self.font_title.render(s.WINDOW_TITLE, True, s.Color.WHITE)
        rect = text.get_rect(center=(s.WINDOW_WIDTH // 2, _TITLE_Y))
        screen.blit(text, rect)

    def _draw_connections(self, screen: pygame.Surface) -> None:
        """Dessine les lignes reliant les nœuds dans l'ordre du serpentin."""
        for i in range(len(NODE_POSITIONS) - 1):
            x1, y1 = NODE_POSITIONS[i]
            x2, y2 = NODE_POSITIONS[i + 1]
            pygame.draw.line(screen, (80, 80, 80), (x1, y1), (x2, y2), 3)

    def _draw_nodes(self, screen: pygame.Surface) -> None:
        for i, (x, y) in enumerate(NODE_POSITIONS):
            self._draw_node(screen, i, x, y)

    def _draw_node(self, screen: pygame.Surface, index: int, x: int, y: int) -> None:
        hovered = self._hovered_level == index
        color = s.Color.BUTTON_HOVER if hovered else s.Color.BUTTON
        border_color = s.Color.WHITE if hovered else (120, 120, 160)

        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, border_color, (x, y), NODE_RADIUS, 3)

        label = self.font_level.render(str(index + 1), True, s.Color.WHITE)
        label_rect = label.get_rect(center=(x, y))
        screen.blit(label, label_rect)

    def _draw_rules_button(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rules_button_rect.collidepoint(mouse_pos)
        color = s.Color.BUTTON_HOVER if hovered else s.Color.BUTTON
        pygame.draw.rect(screen, color, self.rules_button_rect, border_radius=8)
        label = self.font_button.render("Règles du jeu", True, s.Color.WHITE)
        rect = label.get_rect(center=self.rules_button_rect.center)
        screen.blit(label, rect)

    def _draw_scores_button(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.scores_button_rect.collidepoint(mouse_pos)
        color = (80, 140, 60) if hovered else (60, 110, 45)
        pygame.draw.rect(screen, color, self.scores_button_rect, border_radius=8)
        label = self.font_button.render("Classements", True, s.Color.WHITE)
        rect = label.get_rect(center=self.scores_button_rect.center)
        screen.blit(label, rect)

    def _draw_hint(self, screen: pygame.Surface) -> None:
        text = self.font_hint.render(
            "Cliquez sur un niveau pour jouer", True, (140, 140, 140)
        )
        rect = text.get_rect(center=(s.WINDOW_WIDTH // 2, _HINT_Y))
        screen.blit(text, rect)

    def _draw_rules_screen(self, screen: pygame.Surface) -> None:
        screen.fill(s.Color.BLACK)

        panel = pygame.Surface(
            (s.WINDOW_WIDTH - 80, s.WINDOW_HEIGHT - 60), pygame.SRCALPHA
        )
        panel.fill((10, 10, 20, 220))
        screen.blit(panel, (40, 30))
        pygame.draw.rect(
            screen,
            (80, 80, 140),
            (40, 30, s.WINDOW_WIDTH - 80, s.WINDOW_HEIGHT - 60),
            2,
            border_radius=10,
        )

        title = self.font_title.render("Règles du jeu", True, s.Color.WHITE)
        title_rect = title.get_rect(center=(s.WINDOW_WIDTH // 2, 80))
        screen.blit(title, title_rect)

        font_rules = pygame.font.SysFont(None, 20)
        y = 140
        for line in RULES:
            if line == "":
                y += 8
                continue
            color = s.Color.GOLD if line.startswith("===") else (200, 200, 200)
            text = font_rules.render(line, True, color)
            screen.blit(text, (70, y))
            y += 24

        mouse_pos = pygame.mouse.get_pos()
        hovered = self.back_rect.collidepoint(mouse_pos)
        color = s.Color.BUTTON_HOVER if hovered else s.Color.BUTTON
        pygame.draw.rect(screen, color, self.back_rect, border_radius=8)
        label = self.font_button.render("Retour a la carte", True, s.Color.WHITE)
        label_rect = label.get_rect(center=self.back_rect.center)
        screen.blit(label, label_rect)

    def _get_level_at(self, pos: tuple[int, int]) -> int | None:
        """Retourne l'index du noeud sous la position donnée, ou None."""
        px, py = pos
        for i, (x, y) in enumerate(NODE_POSITIONS):
            if (px - x) ** 2 + (py - y) ** 2 <= NODE_RADIUS**2:
                return i
        return None
