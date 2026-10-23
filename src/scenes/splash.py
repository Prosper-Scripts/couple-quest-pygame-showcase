import pygame

from config import ACCENT, SCREEN_HEIGHT, SCREEN_WIDTH, TEXT
from scenes.base import BaseScene


class SplashScene(BaseScene):
    def __init__(self, state) -> None:
        super().__init__(state)
        self.elapsed = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.next_scene = "menu"

    def update(self, dt: float) -> None:
        self.elapsed += dt
        if self.elapsed >= 2.0:
            self.next_scene = "menu"

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        title = self.state.content.profile.title
        tagline = self.state.content.profile.tagline
        pulse = 1 + (0.02 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() * 0.12).x)
        title_font = pygame.font.SysFont("georgia", int(54 * pulse), bold=True)

        self.draw_text(screen, title, title_font, TEXT, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, center=True)
        self.draw_text(screen, tagline, self.subtitle_font, ACCENT, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 38, center=True)
        self.draw_footer_hint(screen, "Press any key to continue")
        self.finish_frame(screen)
