import pygame

from config import MUTED, TEXT
from scenes.base import BaseScene
from ui.buttons import Button
from ui.cards import Card


class LoveMissionsScene(BaseScene):
    def __init__(self, state) -> None:
        super().__init__(state)
        self.back_button = Button("Back", pygame.Rect(60, 50, 120, 48), subtle=True)
        self.complete_button = Button("Mission Done", pygame.Rect(500, 600, 280, 56))

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.back_button.handle_event(event):
            self.play_sound("click")
            self.next_scene = "mode_select"
        elif self.state.content.challenges and self.complete_button.handle_event(event):
            self.play_sound("win")
            self.show_feedback("Mission complete.", "success")
            self.state.score = 1
            challenge = self.state.content.challenges[self.state.active_challenge_index]
            self.state.add_result(f"Love Missions: Completed '{challenge.title}'.")
            self.next_scene = "results"

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        self.draw_header(screen, "Love Missions", "Tiny playful tasks for your next hangout")
        self.back_button.draw(screen, self.body_font)
        if not self.state.content.challenges:
            self.draw_text(screen, "Add a mission to data/challenges.json to get started.", self.body_font, MUTED, 270, 340)
            self.finish_frame(screen)
            return

        self.complete_button.draw(screen, self.body_font)

        challenge = self.state.content.challenges[self.state.active_challenge_index]
        card = Card(
            rect=self.animate_rect(pygame.Rect(190, 240, 900, 230), delay=0.05),
            title=challenge.title,
            body=f"{challenge.prompt}\n\nReward: {challenge.reward_text}",
        )
        card.draw(screen, self.subtitle_font, self.body_font)
        self.draw_text(screen, "Finish this offline challenge together, then mark it done.", self.body_font, MUTED, 310, 520)
        self.finish_frame(screen)
