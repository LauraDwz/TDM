import pygame
import settings as s

_MONSTER_LABELS = {
    "G": ("Goblin", (60, 160, 60)),
    "O": ("Orc", (200, 50, 50)),
}


class WaveInfoView:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 42)
        self.font_wave = pygame.font.SysFont(None, 26)
        self.font_mono = pygame.font.SysFont(None, 22)
        self.font_button = pygame.font.SysFont(None, 26)

        self.close_rect = pygame.Rect(
            s.WINDOW_WIDTH // 2 + 260, s.WINDOW_HEIGHT // 2 - 240, 32, 32
        )
        self.panel_rect = pygame.Rect(
            s.WINDOW_WIDTH // 2 - 300, s.WINDOW_HEIGHT // 2 - 260, 600, 480
        )

    def draw(
        self,
        screen: pygame.Surface,
        wave_definitions: list[dict],
        current_wave_index: int,
    ) -> None:
        overlay = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (25, 25, 40), self.panel_rect, border_radius=12)
        pygame.draw.rect(screen, (80, 80, 140), self.panel_rect, 2, border_radius=12)

        title = self.font_title.render("Vagues restantes", True, s.Color.WHITE)
        screen.blit(
            title,
            title.get_rect(center=(s.WINDOW_WIDTH // 2, self.panel_rect.top + 30)),
        )

        pygame.draw.line(
            screen,
            (80, 80, 140),
            (self.panel_rect.left + 20, self.panel_rect.top + 55),
            (self.panel_rect.right - 20, self.panel_rect.top + 55),
            1,
        )

        remaining = wave_definitions[current_wave_index:]
        if not remaining:
            msg = self.font_wave.render(
                "Toutes les vagues ont ete lancees !", True, (180, 180, 180)
            )
            screen.blit(
                msg, msg.get_rect(center=(s.WINDOW_WIDTH // 2, self.panel_rect.centery))
            )
        else:
            y = self.panel_rect.top + 70
            for i, wave_def in enumerate(remaining):
                if y > self.panel_rect.bottom - 60:
                    more = self.font_mono.render(
                        f"... et {len(remaining) - i} autre(s)", True, (150, 150, 150)
                    )
                    screen.blit(more, (self.panel_rect.left + 20, y))
                    break

                wave_num = current_wave_index + i + 1
                label = self.font_wave.render(f"Vague {wave_num}", True, s.Color.GOLD)
                screen.blit(label, (self.panel_rect.left + 20, y))

                counts = {}
                for m in wave_def["monsters"]:
                    t = m["type"]
                    counts[t] = counts.get(t, 0) + 1

                x = self.panel_rect.left + 130
                for code, count in counts.items():
                    name, color = _MONSTER_LABELS.get(code, (code, s.Color.WHITE))
                    text = self.font_mono.render(f"{count}x {name}", True, color)
                    screen.blit(text, (x, y + 2))
                    x += text.get_width() + 20

                if i == 0:
                    interval_txt = self.font_mono.render(
                        f"  (spawn: {wave_def['spawn_interval']}s)",
                        True,
                        (140, 140, 140),
                    )
                    screen.blit(interval_txt, (x, y + 2))

                y += 32

        mouse_pos = pygame.mouse.get_pos()
        close_color = (
            (180, 60, 60) if self.close_rect.collidepoint(mouse_pos) else (120, 40, 40)
        )
        pygame.draw.circle(screen, close_color, self.close_rect.center, 16)
        cross = self.font_button.render("x", True, s.Color.WHITE)
        screen.blit(cross, cross.get_rect(center=self.close_rect.center))

    def handle_click(self, pos: tuple[int, int]) -> bool:
        """Retourne True si le clic ferme l'overlay (croix ou clic hors panneau)"""
        if self.close_rect.collidepoint(pos):
            return True
        if not self.panel_rect.collidepoint(pos):
            return True
        return False
