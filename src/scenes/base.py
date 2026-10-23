import math

import pygame

from config import (
    ACCENT,
    BACKGROUND,
    FONT_NAME,
    MUTED,
    PANEL,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHADOW,
    SUCCESS,
    TEXT,
    WARNING,
)
from game.state import GameState


class BaseScene:
    def __init__(self, state: GameState) -> None:
        self.state = state
        self.is_running = True
        self.next_scene: str | None = None
        self.entered_at = pygame.time.get_ticks() / 1000
        self.title_font = pygame.font.SysFont(FONT_NAME, 54, bold=True)
        self.subtitle_font = pygame.font.SysFont(FONT_NAME, 28)
        self.body_font = pygame.font.SysFont(FONT_NAME, 22)
        self.small_font = pygame.font.SysFont(FONT_NAME, 18)

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, dt: float) -> None:
        return None

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND)
        self.draw_background_glow(screen)

    def draw_text(
        self,
        screen: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        x: int,
        y: int,
        center: bool = False,
    ) -> None:
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        screen.blit(surface, rect)

    def draw_panel(self, screen: pygame.Surface, rect: pygame.Rect) -> None:
        shadow_rect = rect.move(8, 8)
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=24)
        pygame.draw.rect(screen, PANEL, rect, border_radius=24)

    def draw_header(self, screen: pygame.Surface, title: str, subtitle: str) -> None:
        self.draw_text(screen, title, self.title_font, TEXT, SCREEN_WIDTH // 2, 70, center=True)
        self.draw_text(screen, subtitle, self.subtitle_font, MUTED, SCREEN_WIDTH // 2, 120, center=True)
        pygame.draw.line(screen, ACCENT, (200, 155), (SCREEN_WIDTH - 200, 155), 3)

    def draw_footer_hint(self, screen: pygame.Surface, text: str) -> None:
        self.draw_text(screen, text, self.small_font, MUTED, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 28, center=True)

    def scene_elapsed(self) -> float:
        return (pygame.time.get_ticks() / 1000) - self.entered_at

    def intro_progress(self, delay: float = 0.0, duration: float = 0.55) -> float:
        progress = max(0.0, min(1.0, (self.scene_elapsed() - delay) / duration))
        return 1 - (1 - progress) ** 3

    def animate_rect(self, rect: pygame.Rect, delay: float = 0.0, distance: int = 28) -> pygame.Rect:
        progress = self.intro_progress(delay)
        offset = int((1 - progress) * distance)
        return rect.move(0, offset)

    def draw_background_glow(self, screen: pygame.Surface) -> None:
        elapsed = self.scene_elapsed()
        glow_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        circles = [
            ((220, 120, 160, 28), int(120 + math.sin(elapsed * 1.2) * 20), 100, 120),
            ((255, 214, 187, 24), SCREEN_WIDTH - 160, int(170 + math.cos(elapsed * 0.9) * 18), 150),
            ((236, 189, 162, 18), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110, 140),
        ]

        for color, x, y, radius in circles:
            pygame.draw.circle(glow_surface, color, (x, y), radius)

        screen.blit(glow_surface, (0, 0))

    def play_sound(self, name: str) -> None:
        if self.state.audio is not None:
            self.state.audio.play(name)

    def show_feedback(self, message: str, kind: str) -> None:
        color_map = {
            "success": SUCCESS,
            "warning": WARNING,
            "neutral": ACCENT,
        }
        self.state.set_feedback(message, color_map.get(kind, TEXT))

    def draw_feedback_banner(self, screen: pygame.Surface) -> None:
        if self.state.feedback_timer <= 0 or not self.state.feedback_message:
            return

        alpha = int(255 * min(1.0, self.state.feedback_timer / 0.25, self.state.feedback_timer))
        banner = pygame.Surface((420, 50), pygame.SRCALPHA)
        color = (*self.state.feedback_color, alpha)
        text_color = (255, 250, 246, alpha)
        pygame.draw.rect(banner, color, banner.get_rect(), border_radius=18)
        text_surface = self.body_font.render(self.state.feedback_message, True, text_color[:3])
        text_surface.set_alpha(alpha)
        banner.blit(text_surface, text_surface.get_rect(center=banner.get_rect().center))
        screen.blit(banner, (SCREEN_WIDTH // 2 - 210, 20))

    def draw_intro_overlay(self, screen: pygame.Surface) -> None:
        overlay_alpha = int((1 - self.intro_progress()) * 180)
        if overlay_alpha <= 0:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BACKGROUND)
        overlay.set_alpha(overlay_alpha)
        screen.blit(overlay, (0, 0))

    def finish_frame(self, screen: pygame.Surface) -> None:
        self.draw_intro_overlay(screen)
        self.draw_feedback_banner(screen)
