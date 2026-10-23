import pygame

from config import MUTED, SCREEN_WIDTH, TEXT
from scenes.base import BaseScene
from ui.buttons import Button


class ResultsScene(BaseScene):
    def __init__(self, state) -> None:
        super().__init__(state)
        self.play_again_button = Button("Play Another Mode", pygame.Rect(360, 600, 280, 56))
        self.menu_button = Button("Main Menu", pygame.Rect(680, 600, 240, 56), subtle=True)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.play_again_button.handle_event(event):
            self.play_sound("click")
            self.next_scene = "mode_select"
        elif self.menu_button.handle_event(event):
            self.play_sound("click")
            self.next_scene = "menu"

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        self.draw_header(screen, "Round Complete", "A soft summary of your latest session")
        self.draw_text(screen, f"Mode: {self.state.current_mode.replace('_', ' ').title()}", self.body_font, TEXT, SCREEN_WIDTH // 2, 210, center=True)
        self.draw_text(screen, f"Score: {self.state.score}", self.subtitle_font, TEXT, SCREEN_WIDTH // 2, 255, center=True)
        self.draw_text(screen, f"Hearts left: {self.state.hearts}", self.body_font, MUTED, SCREEN_WIDTH // 2, 295, center=True)

        panel = self.animate_rect(pygame.Rect(170, 340, 940, 200), delay=0.05)
        self.draw_panel(screen, panel)
        summary = self.state.session_summary[-4:] or ["Round finished. Select another mode to keep playing."]
        for index, item in enumerate(summary):
            self.draw_text(screen, item, self.body_font, TEXT, panel.x + 40, panel.y + 40 + (index * 38))

        self.play_again_button.draw(screen, self.body_font)
        self.menu_button.draw(screen, self.body_font)
        self.finish_frame(screen)
