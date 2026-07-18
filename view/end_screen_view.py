import pygame
import settings as s

_DEFEAT_TIPS = [
    "Fusionnez vos unites : deux unites de meme type",
    "et meme niveau donnent une unite bien plus forte.",
    "",
    "Placez vos unites au plus pres du chemin pour",
    "maximiser le nombre de monstres touches.",
    "",
    "Les Mages font beaucoup de degats sur les Orcs.",
    "Les Archers sont ideaux pour les Gobelins rapides.",
    "",
    "Utilisez vos boosters au bon moment : le booster",
    "Or en debut de partie maximise vos achats.",
]


class EndScreenView:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 64)
        self.font_sub = pygame.font.SysFont(None, 36)
        self.font_stat = pygame.font.SysFont(None, 28)
        self.font_tip = pygame.font.SysFont(None, 22)
        self.font_button = pygame.font.SysFont(None, 28)

        btn_w, btn_h = 280, 50
        cx = s.WINDOW_WIDTH // 2

        self.next_level_rect = pygame.Rect(cx - btn_w // 2, 500, btn_w, btn_h)
        self.scores_rect = pygame.Rect(cx - btn_w // 2, 562, btn_w, btn_h)
        self.map_rect_victory = pygame.Rect(cx - btn_w // 2, 624, btn_w, btn_h)
        self.restart_rect = pygame.Rect(cx - btn_w // 2, 510, btn_w, btn_h)
        self.map_rect_defeat = pygame.Rect(cx - btn_w // 2, 575, btn_w, btn_h)

    def draw_victory(
        self, screen: pygame.Surface, game_state, has_next_level: bool
    ) -> None:
        self._draw_overlay(screen, (0, 0, 0, 200))
        self._draw_victory_content(screen, game_state, has_next_level)

    def draw_defeat(self, screen: pygame.Surface) -> None:
        self._draw_overlay(screen, (0, 0, 0, 210))
        self._draw_defeat_content(screen)

    def _draw_overlay(self, screen: pygame.Surface, color: tuple) -> None:
        overlay = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(color)
        screen.blit(overlay, (0, 0))

    def _draw_victory_content(
        self, screen: pygame.Surface, game_state, has_next_level: bool
    ) -> None:
        title = self.font_title.render("VICTOIRE !", True, s.Color.GOLD)
        screen.blit(title, title.get_rect(center=(s.WINDOW_WIDTH // 2, 110)))

        sub = self.font_sub.render(
            "Vous avez survecu a toutes les vagues !", True, s.Color.WHITE
        )
        screen.blit(sub, sub.get_rect(center=(s.WINDOW_WIDTH // 2, 175)))

        pygame.draw.line(
            screen,
            s.Color.GOLD,
            (s.WINDOW_WIDTH // 2 - 200, 205),
            (s.WINDOW_WIDTH // 2 + 200, 205),
            1,
        )

        elapsed = game_state.elapsed_time
        minutes = int(elapsed) // 60
        seconds = int(elapsed) % 60
        stats = [
            ("Temps", f"{minutes}m {seconds:02d}s"),
            ("Score", str(game_state.score)),
            ("Or restant", str(game_state.gold)),
            ("Vies restantes", str(game_state.lives)),
        ]

        for i, (label, value) in enumerate(stats):
            y = 225 + i * 52
            pygame.draw.rect(
                screen,
                (30, 30, 30),
                (s.WINDOW_WIDTH // 2 - 220, y, 440, 40),
                border_radius=8,
            )
            lbl = self.font_stat.render(label, True, (180, 180, 180))
            val = self.font_stat.render(value, True, s.Color.WHITE)
            screen.blit(lbl, lbl.get_rect(midleft=(s.WINDOW_WIDTH // 2 - 200, y + 20)))
            screen.blit(val, val.get_rect(midright=(s.WINDOW_WIDTH // 2 + 200, y + 20)))

        mouse_pos = pygame.mouse.get_pos()
        if has_next_level:
            self._draw_button(
                screen,
                self.next_level_rect,
                "Niveau suivant",
                mouse_pos,
                highlight=True,
            )
        self._draw_button(screen, self.scores_rect, "Voir les classements", mouse_pos)
        self._draw_button(screen, self.map_rect_victory, "Carte des niveaux", mouse_pos)

    def _draw_defeat_content(self, screen: pygame.Surface) -> None:
        title = self.font_title.render("DEFAITE", True, s.Color.HEART)
        screen.blit(title, title.get_rect(center=(s.WINDOW_WIDTH // 2, 100)))

        sub = self.font_sub.render(
            "Vos defenses ont ete submergees...", True, (200, 200, 200)
        )
        screen.blit(sub, sub.get_rect(center=(s.WINDOW_WIDTH // 2, 155)))

        pygame.draw.line(
            screen,
            s.Color.HEART,
            (s.WINDOW_WIDTH // 2 - 200, 185),
            (s.WINDOW_WIDTH // 2 + 200, 185),
            1,
        )

        tip_title = self.font_stat.render("Conseils :", True, s.Color.GOLD)
        screen.blit(tip_title, (s.WINDOW_WIDTH // 2 - 220, 200))

        y = 235
        for line in _DEFEAT_TIPS:
            if line == "":
                y += 8
                continue
            tip = self.font_tip.render(line, True, (200, 200, 200))
            screen.blit(tip, (s.WINDOW_WIDTH // 2 - 220, y))
            y += 22

        mouse_pos = pygame.mouse.get_pos()
        self._draw_button(
            screen,
            self.restart_rect,
            "Recommencer le niveau",
            mouse_pos,
            highlight=True,
        )
        self._draw_button(screen, self.map_rect_defeat, "Carte des niveaux", mouse_pos)

    def _draw_button(self, screen, rect, label, mouse_pos, highlight=False) -> None:
        if highlight:
            base = (80, 140, 60) if rect.collidepoint(mouse_pos) else (60, 110, 45)
        else:
            base = (
                s.Color.BUTTON_HOVER if rect.collidepoint(mouse_pos) else s.Color.BUTTON
            )
        pygame.draw.rect(screen, base, rect, border_radius=8)
        text = self.font_button.render(label, True, s.Color.WHITE)
        screen.blit(text, text.get_rect(center=rect.center))

    def handle_click_victory(self, pos: tuple, has_next_level: bool) -> str | None:
        """Retourne next, scores, map ou None, le résultat sera géré dans game.py"""
        if has_next_level and self.next_level_rect.collidepoint(pos):
            return "next"
        if self.scores_rect.collidepoint(pos):
            return "scores"
        if self.map_rect_victory.collidepoint(pos):
            return "map"
        return None

    def handle_click_defeat(self, pos: tuple) -> str | None:
        """Retourne restart, map ou None, le résultat sera géré dans game.py"""
        if self.restart_rect.collidepoint(pos):
            return "restart"
        if self.map_rect_defeat.collidepoint(pos):
            return "map"
        return None
