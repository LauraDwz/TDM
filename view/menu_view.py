import pygame
import settings as s
from data.rules import RULES


class MenuView:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 52)
        self.font_button = pygame.font.SysFont(None, 28)
        self.font_rules = pygame.font.SysFont(None, 20)

        button_w = 260
        button_h = 50
        center_x = s.WINDOW_WIDTH // 2

        self.resume_rect = pygame.Rect(
            center_x - button_w // 2, 240, button_w, button_h
        )
        self.restart_rect = pygame.Rect(
            center_x - button_w // 2, 305, button_w, button_h
        )
        self.rules_rect = pygame.Rect(center_x - button_w // 2, 370, button_w, button_h)
        self.map_rect = pygame.Rect(center_x - button_w // 2, 435, button_w, button_h)
        self.quit_rect = pygame.Rect(center_x - button_w // 2, 565, button_w, button_h)
        self.back_rect = pygame.Rect(center_x - 160, 710, 320, 44)

        icon_w = 125
        icon_h = 50
        icon_y = 500
        self.music_btn_rect = pygame.Rect(center_x - icon_w - 5, icon_y, icon_w, icon_h)
        self.sfx_btn_rect = pygame.Rect(center_x + 5, icon_y, icon_w, icon_h)

        self._show_rules = False

    def toggle_rules(self) -> None:
        self._show_rules = not self._show_rules

    def reset(self) -> None:
        """Réinitialise l'état interne du menu. À appeler à chaque fermeture"""
        self._show_rules = False

    def draw(self, screen: pygame.Surface, sound_manager=None) -> None:
        self._draw_overlay(screen)
        if self._show_rules:
            self._draw_rules(screen)
        else:
            self._draw_main_menu(screen, sound_manager)

    def _draw_overlay(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

    def _draw_main_menu(self, screen: pygame.Surface, sound_manager=None) -> None:
        title = self.font_title.render("PAUSE", True, s.Color.WHITE)
        title_rect = title.get_rect(center=(s.WINDOW_WIDTH // 2, 200))
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        self._draw_button(screen, self.resume_rect, "Reprendre", mouse_pos)
        self._draw_button(screen, self.restart_rect, "Recommencer le niveau", mouse_pos)
        self._draw_button(screen, self.rules_rect, "Règles du jeu", mouse_pos)
        self._draw_button(screen, self.map_rect, "Carte des niveaux", mouse_pos)
        if sound_manager is not None:
            self._draw_icon_button(
                screen,
                self.music_btn_rect,
                "music",
                sound_manager.music_enabled,
                mouse_pos,
            )
            self._draw_icon_button(
                screen, self.sfx_btn_rect, "sfx", sound_manager.sfx_enabled, mouse_pos
            )
        self._draw_button(screen, self.quit_rect, "Quitter", mouse_pos, danger=True)

    def _draw_button(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        label: str,
        mouse_pos: tuple,
        danger: bool = False,
        custom_color: tuple = None,
    ) -> None:
        if custom_color:
            r, g, b = custom_color
            color = (
                (min(255, r + 20), min(255, g + 20), min(255, b + 20))
                if rect.collidepoint(mouse_pos)
                else custom_color
            )
        elif danger:
            color = (160, 40, 40) if rect.collidepoint(mouse_pos) else (120, 30, 30)
        else:
            color = (
                s.Color.BUTTON_HOVER if rect.collidepoint(mouse_pos) else s.Color.BUTTON
            )
        pygame.draw.rect(screen, color, rect, border_radius=8)
        text = self.font_button.render(label, True, s.Color.WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def _draw_icon_button(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        kind: str,
        enabled: bool,
        mouse_pos: tuple,
    ) -> None:
        """Dessine un bouton icône musique ou son avec état ON/OFF"""
        bg = (50, 130, 70) if enabled else (80, 80, 80)
        if rect.collidepoint(mouse_pos):
            bg = tuple(min(255, c + 20) for c in bg)
        pygame.draw.rect(screen, bg, rect, border_radius=8)
        pygame.draw.rect(screen, (150, 150, 150), rect, 1, border_radius=8)

        cx, cy = rect.centerx - 10, rect.centery

        if kind == "music":
            self._draw_music_note(screen, cx, cy)
        else:
            self._draw_speaker(screen, cx, cy, enabled)

        font = pygame.font.SysFont(None, 20)
        label = font.render("ON" if enabled else "OFF", True, s.Color.WHITE)
        screen.blit(label, label.get_rect(midleft=(cx + 22, cy)))

        if not enabled:
            x1 = rect.left + 8
            y1 = rect.bottom - 8
            x2 = rect.right - 8
            y2 = rect.top + 8
            pygame.draw.line(screen, (220, 60, 60), (x1, y1), (x2, y2), 2)

    def _draw_music_note(self, screen: pygame.Surface, cx: int, cy: int) -> None:
        """Dessine une note de musique"""
        color = s.Color.WHITE
        pygame.draw.ellipse(screen, color, (cx - 6, cy + 2, 10, 7))
        pygame.draw.line(screen, color, (cx + 4, cy + 5), (cx + 4, cy - 10), 2)
        pygame.draw.line(screen, color, (cx + 4, cy - 10), (cx + 12, cy - 7), 2)

    def _draw_speaker(
        self, screen: pygame.Surface, cx: int, cy: int, enabled: bool
    ) -> None:
        """Dessine un haut-parleur"""
        color = s.Color.WHITE
        speaker = [
            (cx - 6, cy - 5),
            (cx, cy - 5),
            (cx + 6, cy - 10),
            (cx + 6, cy + 10),
            (cx, cy + 5),
            (cx - 6, cy + 5),
        ]
        pygame.draw.polygon(screen, color, speaker)
        if enabled:
            pygame.draw.arc(screen, color, (cx + 7, cy - 6, 8, 12), -0.6, 0.6, 2)
            pygame.draw.arc(screen, color, (cx + 10, cy - 9, 10, 18), -0.6, 0.6, 2)

    def _draw_rules(self, screen: pygame.Surface) -> None:
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
        title_rect = title.get_rect(center=(s.WINDOW_WIDTH // 2, 75))
        screen.blit(title, title_rect)

        y = 125
        for line in RULES:
            if line == "":
                y += 8
                continue
            color = s.Color.GOLD if line.startswith("===") else s.Color.HUD_TEXT
            text = self.font_rules.render(line, True, color)
            screen.blit(text, (70, y))
            y += 24

        mouse_pos = pygame.mouse.get_pos()
        self._draw_button(screen, self.back_rect, "Retour", mouse_pos)

    def handle_click(self, pos: tuple[int, int]) -> str | None:
        if self._show_rules:
            if self.back_rect.collidepoint(pos):
                self._show_rules = False
            return None

        if self.resume_rect.collidepoint(pos):
            return "resume"
        if self.restart_rect.collidepoint(pos):
            return "restart"
        if self.rules_rect.collidepoint(pos):
            self.toggle_rules()
            return None
        if self.map_rect.collidepoint(pos):
            return "map"
        if self.music_btn_rect.collidepoint(pos):
            return "mute_music"
        if self.sfx_btn_rect.collidepoint(pos):
            return "mute_sfx"
        if self.quit_rect.collidepoint(pos):
            return "quit"
        return None
