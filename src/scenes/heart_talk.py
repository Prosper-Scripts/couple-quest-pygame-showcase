import pygame

from config import MUTED, TEXT
from scenes.base import BaseScene
from ui.buttons import Button
from ui.cards import Card


class HeartTalkScene(BaseScene):
    def __init__(self, state) -> None:
        super().__init__(state)
        self.back_button = Button("Back", pygame.Rect(60, 50, 120, 48), subtle=True)
        self.next_button = Button("Next Card", pygame.Rect(470, 600, 180, 56))
        self.finish_button = Button("End Talk", pygame.Rect(680, 600, 180, 56), subtle=True)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.back_button.handle_event(event):
            self.play_sound("click")
            self.next_scene = "mode_select"
            return

        question = self.state.active_question()
        if question is None:
            self.next_scene = "results"
            return

        if self.next_button.handle_event(event):
            self.play_sound("click")
            self.show_feedback("One more layer deeper.", "neutral")
            self.state.score += 1
            self.state.add_result(f"Heart Talk: You explored '{question.prompt[:52]}...'.")
            self.state.current_question_index += 1
            if self.state.current_question_index >= len(self.state.session_questions):
                self.next_scene = "results"
        elif self.finish_button.handle_event(event):
            self.play_sound("transition")
            self.next_scene = "results"

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        self.draw_header(screen, "Heart Talk", "Slow down, talk deeply, and dream about the future together")
        self.back_button.draw(screen, self.body_font)
        self.next_button.draw(screen, self.body_font)
        self.finish_button.draw(screen, self.body_font)

        question = self.state.active_question()
        if question is None:
            self.draw_text(screen, "No deep-talk prompts yet. Add more in data/questions.json.", self.body_font, MUTED, 340, 360)
            return

        category_label = question.category.replace("_", " ").title()
        card = Card(
            rect=self.animate_rect(pygame.Rect(150, 210, 980, 300), delay=0.05),
            title=f"{category_label} Card",
            body=question.prompt,
        )
        card.draw(screen, self.subtitle_font, self.body_font)

        self.draw_text(screen, f"Card {self.state.current_question_index + 1} of {len(self.state.session_questions)}", self.body_font, TEXT, 150, 540)
        self.draw_text(screen, "Tip: answer fully, then ask one follow-up before moving on.", self.body_font, MUTED, 150, 575)
        self.finish_frame(screen)
