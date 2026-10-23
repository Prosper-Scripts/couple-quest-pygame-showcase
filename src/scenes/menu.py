import pygame

from config import MUTED, SCREEN_HEIGHT, SCREEN_WIDTH, TEXT
from scenes.base import BaseScene
from ui.buttons import Button


class MenuScene(BaseScene):
    def __init__(self, state) -> None:
        super().__init__(state)
        self.start_button = Button("Start Our Game", pygame.Rect(480, 420, 320, 64))
        self.quit_button = Button("Exit", pygame.Rect(560, 500, 160, 56), subtle=True)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.start_button.handle_event(event):
            self.play_sound("start")
            self.next_scene = "mode_select"
        if self.quit_button.handle_event(event):
            self.play_sound("click")
            self.is_running = False

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        profile = self.state.content.profile
        self.draw_text(screen, profile.title, self.title_font, TEXT, SCREEN_WIDTH // 2, 120, center=True)
        self.draw_text(screen, profile.home_message, self.subtitle_font, MUTED, SCREEN_WIDTH // 2, 175, center=True)

        panel = self.animate_rect(pygame.Rect(240, 240, 800, 120), delay=0.05)
        self.draw_panel(screen, panel)
        self.draw_text(screen, f"{profile.partner_one} + {profile.partner_two}", self.subtitle_font, TEXT, panel.x + 40, panel.y + 35)
        self.draw_text(screen, f"Together for {profile.years_together} years", self.body_font, MUTED, panel.x + 40, panel.y + 75)
        self.draw_text(screen, f"Anniversary: {profile.anniversary}", self.body_font, MUTED, panel.x + 380, panel.y + 75)

        self.start_button.draw(screen, self.body_font)
        self.quit_button.draw(screen, self.body_font)
        self.draw_footer_hint(screen, "Best played side by side, with honesty, laughter, and a little teasing")
        self.finish_frame(screen)
