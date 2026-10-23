import pygame

from config import MUTED, TEXT
from scenes.base import BaseScene
from ui.buttons import Button
from ui.cards import Card


class WhoSaidItScene(BaseScene):
    def __init__(self, state) -> None:
        super().__init__(state)
        self.back_button = Button("Back", pygame.Rect(60, 50, 120, 48), subtle=True)
        self.player_one_button = Button(self.state.content.profile.partner_one, pygame.Rect(300, 460, 260, 64))
        self.player_two_button = Button(self.state.content.profile.partner_two, pygame.Rect(720, 460, 260, 64))

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.back_button.handle_event(event):
            self.play_sound("click")
            self.next_scene = "mode_select"
            return

        question = self.state.active_question()
        if question is None:
            self.next_scene = "results"
            return

        selected = None
        if self.player_one_button.handle_event(event):
            selected = self.state.content.profile.partner_one
        elif self.player_two_button.handle_event(event):
            selected = self.state.content.profile.partner_two

        if selected is not None:
            if selected == question.answer:
                self.play_sound("correct")
                self.show_feedback("You remembered who said it.", "success")
                self.state.score += 1
                self.state.add_result(f"Who Said It?: You matched '{question.prompt[:44]}...'.")
            else:
                self.play_sound("wrong")
                self.show_feedback("Close, but not this one.", "warning")
                self.state.hearts -= 1
                self.state.add_result(f"Who Said It?: You guessed wrong on '{question.prompt[:44]}...'.")

            self.state.current_question_index += 1
            if self.state.current_question_index >= len(self.state.session_questions) or self.state.hearts <= 0:
                self.next_scene = "results"

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        self.draw_header(screen, "Who Said It?", "Guess which one of you said the quote or did the thing")
        self.back_button.draw(screen, self.body_font)

        question = self.state.active_question()
        prompt = question.prompt if question is not None else "No quote cards yet. Add more in data/questions.json."
        card = Card(
            rect=self.animate_rect(pygame.Rect(220, 220, 840, 170), delay=0.05),
            title="Quote Card",
            body=prompt,
        )
        card.draw(screen, self.subtitle_font, self.body_font)
        self.player_one_button.draw(screen, self.body_font)
        self.player_two_button.draw(screen, self.body_font)
        self.draw_text(screen, "These prompts work best with real quotes, habits, and origin-story moments.", self.body_font, MUTED, 260, 560)
        self.draw_text(screen, f"Score: {self.state.score} | Hearts: {self.state.hearts}", self.body_font, TEXT, 470, 600)
        self.finish_frame(screen)
