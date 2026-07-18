import pygame
import settings as s
from data.scoreboard import get_scores, get_all_scores

_RANK_LABELS = ["1.", "2.", "3."]
_RANK_COLORS = [(255, 200, 0), (180, 180, 180), (180, 100, 40)]


class ScoreboardView:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 48)
        self.font_level = pygame.font.SysFont(None, 28)
        self.font_entry = pygame.font.SysFont(None, 24)
        self.font_button = pygame.font.SysFont(None, 26)
        self.font_empty = pygame.font.SysFont(None, 22)

        self.panel_rect = pygame.Rect(
            s.WINDOW_WIDTH // 2 - 320, s.WINDOW_HEIGHT // 2 - 280, 640, 540
        )
        self.close_rect = pygame.Rect(
            self.panel_rect.right - 40, self.panel_rect.top + 8, 32, 32
        )

        self._page = 0
        self._levels_per_page = 4
        self.prev_rect = pygame.Rect(
            self.panel_rect.left + 20, self.panel_rect.bottom - 50, 100, 36
        )
        self.next_rect = pygame.Rect(
            self.panel_rect.right - 120, self.panel_rect.bottom - 50, 100, 36
        )

    def reset(self) -> None:
        self._page = 0

    def draw(
        self, screen: pygame.Surface, total_levels: int, level_index: int | None = None
    ) -> None:
        """Si level_index est fourni, affiche uniquement ce niveau (mode victoire), sinon affiche tous les niveaux paginés (mode carte)"""
        self._draw_overlay(screen)
        self._draw_panel(screen)

        if level_index is not None:
            self._draw_single_level(screen, level_index)
        else:
            self._draw_all_levels(screen, total_levels)

        self._draw_close(screen)

    def _draw_overlay(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

    def _draw_panel(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (20, 20, 35), self.panel_rect, border_radius=12)
        pygame.draw.rect(screen, (80, 80, 160), self.panel_rect, 2, border_radius=12)

    def _draw_close(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        color = (
            (180, 50, 50) if self.close_rect.collidepoint(mouse_pos) else (120, 30, 30)
        )
        pygame.draw.circle(screen, color, self.close_rect.center, 16)
        label = self.font_button.render("x", True, s.Color.WHITE)
        screen.blit(label, label.get_rect(center=self.close_rect.center))

    def _draw_single_level(self, screen: pygame.Surface, level_index: int) -> None:
        """Affiche le top 3 d'un seul niveau (mode écran de victoire)"""
        title = self.font_title.render(
            f"Scores — Niveau {level_index + 1}", True, s.Color.GOLD
        )
        screen.blit(
            title,
            title.get_rect(center=(s.WINDOW_WIDTH // 2, self.panel_rect.top + 40)),
        )

        pygame.draw.line(
            screen,
            (80, 80, 160),
            (self.panel_rect.left + 20, self.panel_rect.top + 65),
            (self.panel_rect.right - 20, self.panel_rect.top + 65),
            1,
        )

        entries = get_scores(level_index)
        if not entries:
            msg = self.font_empty.render(
                "Aucun score enregistré pour ce niveau.", True, (160, 160, 160)
            )
            screen.blit(
                msg, msg.get_rect(center=(s.WINDOW_WIDTH // 2, self.panel_rect.centery))
            )
            return

        y = self.panel_rect.top + 90
        for i, entry in enumerate(entries):
            self._draw_entry(screen, i, entry, self.panel_rect.left + 40, y, wide=True)
            y += 110

    def _draw_all_levels(self, screen: pygame.Surface, total_levels: int) -> None:
        """Affiche 4 niveaux par page."""
        title = self.font_title.render("Classements", True, s.Color.GOLD)
        screen.blit(
            title,
            title.get_rect(center=(s.WINDOW_WIDTH // 2, self.panel_rect.top + 35)),
        )

        pygame.draw.line(
            screen,
            (80, 80, 160),
            (self.panel_rect.left + 20, self.panel_rect.top + 60),
            (self.panel_rect.right - 20, self.panel_rect.top + 60),
            1,
        )

        all_scores = get_all_scores()
        start = self._page * self._levels_per_page
        end = min(start + self._levels_per_page, total_levels)

        col_w = (self.panel_rect.width - 40) // 2
        for i, level_num in enumerate(range(start + 1, end + 1)):
            col = i % 2
            row = i // 2
            x = self.panel_rect.left + 20 + col * col_w
            y = self.panel_rect.top + 75 + row * 200

            lbl = self.font_level.render(f"Niveau {level_num}", True, s.Color.WHITE)
            screen.blit(lbl, (x + 8, y))
            pygame.draw.line(
                screen, (60, 60, 100), (x, y + 26), (x + col_w - 10, y + 26), 1
            )

            entries = all_scores.get(str(level_num), [])
            if not entries:
                msg = self.font_empty.render("Pas encore joué", True, (100, 100, 100))
                screen.blit(msg, (x + 8, y + 36))
            else:
                for j, entry in enumerate(entries):
                    self._draw_entry(
                        screen, j, entry, x + 8, y + 36 + j * 48, wide=False
                    )

        max_page = max(0, (total_levels - 1) // self._levels_per_page)
        mouse_pos = pygame.mouse.get_pos()

        if self._page > 0:
            c = (
                s.Color.BUTTON_HOVER
                if self.prev_rect.collidepoint(mouse_pos)
                else s.Color.BUTTON
            )
            pygame.draw.rect(screen, c, self.prev_rect, border_radius=6)
            screen.blit(
                self.font_button.render("Precedent", True, s.Color.WHITE),
                self.font_button.render("Precedent", True, s.Color.WHITE).get_rect(
                    center=self.prev_rect.center
                ),
            )

        if self._page < max_page:
            c = (
                s.Color.BUTTON_HOVER
                if self.next_rect.collidepoint(mouse_pos)
                else s.Color.BUTTON
            )
            pygame.draw.rect(screen, c, self.next_rect, border_radius=6)
            screen.blit(
                self.font_button.render("Suivant", True, s.Color.WHITE),
                self.font_button.render("Suivant", True, s.Color.WHITE).get_rect(
                    center=self.next_rect.center
                ),
            )

        page_txt = self.font_empty.render(
            f"Page {self._page + 1}/{max_page + 1}", True, (140, 140, 140)
        )
        screen.blit(
            page_txt,
            page_txt.get_rect(
                center=(s.WINDOW_WIDTH // 2, self.panel_rect.bottom - 32)
            ),
        )

    def _draw_entry(
        self, screen: pygame.Surface, rank: int, entry: dict, x: int, y: int, wide: bool
    ) -> None:
        color = _RANK_COLORS[rank] if rank < 3 else s.Color.HUD_TEXT
        label = _RANK_LABELS[rank] if rank < 3 else f"{rank+1}."

        minutes = int(entry["time"]) // 60
        seconds = int(entry["time"]) % 60
        lives = entry.get(
            "lives_remaining", s.STARTING_LIVES - entry.get("lives_lost", 0)
        )

        if wide:
            pygame.draw.rect(
                screen,
                (35, 35, 55),
                (x, y, self.panel_rect.width - 80, 90),
                border_radius=8,
            )
            screen.blit(self.font_level.render(label, True, color), (x + 14, y + 10))
            screen.blit(
                self.font_entry.render(
                    f"Score : {entry['score']}", True, s.Color.WHITE
                ),
                (x + 14, y + 38),
            )
            screen.blit(
                self.font_entry.render(
                    f"Temps : {minutes}m {seconds:02d}s", True, (180, 180, 180)
                ),
                (x + 180, y + 38),
            )
            screen.blit(
                self.font_entry.render(
                    f"Vies restantes : {lives}", True, (180, 180, 180)
                ),
                (x + 14, y + 62),
            )
        else:
            line = f"{label}  {entry['score']} pts  {minutes}m{seconds:02d}s  {lives} vie(s)"
            screen.blit(self.font_empty.render(line, True, color), (x, y))

    def handle_click(
        self, pos: tuple, total_levels: int, level_index: int | None
    ) -> bool:
        """Retourne True si l'overlay doit se fermer"""
        if self.close_rect.collidepoint(pos):
            return True
        if not self.panel_rect.collidepoint(pos):
            return True
        if level_index is None:
            max_page = max(0, (total_levels - 1) // self._levels_per_page)
            if self.prev_rect.collidepoint(pos) and self._page > 0:
                self._page -= 1
            elif self.next_rect.collidepoint(pos) and self._page < max_page:
                self._page += 1
        return False
