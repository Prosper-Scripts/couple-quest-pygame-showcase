import pygame

from config import MUTED, SCREEN_WIDTH, TEXT
from game.scoring import grade_memory_answer
from scenes.base import BaseScene
from ui.buttons import Button
from ui.cards import Card


class MemoryLaneScene(BaseScene):
    def __init__(self, state) -> None:
        super().__init__(state)
        question = self.state.active_question()
        options = question.options if question else []
        self.option_buttons = []
        start_y = 380
        for index, option in enumerate(options):
            rect = pygame.Rect(260, start_y + (index * 72), 760, 56)
            self.option_buttons.append(Button(option, rect))
        self.back_button = Button("Back", pygame.Rect(60, 50, 120, 48), subtle=True)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.back_button.handle_event(event):
            self.play_sound("click")
            self.next_scene = "mode_select"
            return

        question = self.state.active_question()
        if question is None:
            self.next_scene = "results"
            return

        for button in self.option_buttons:
            if button.handle_event(event):
                if grade_memory_answer(button.label, question.answer):
                    self.play_sound("correct")
                    self.show_feedback("Sweet, that's right.", "success")
                    self.state.score += 1
                    self.state.add_result(f"Memory Lane: You got '{question.prompt}' right.")
                else:
                    self.play_sound("wrong")
                    self.show_feedback("Not quite. Try the next one.", "warning")
                    self.state.hearts -= 1
                    self.state.add_result(f"Memory Lane: You missed '{question.prompt}'.")

                self.state.current_question_index += 1
                if self.state.current_question_index >= len(self.state.session_questions) or self.state.hearts <= 0:
                    self.next_scene = "results"
                else:
                    self.__init__(self.state)
                break

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        self.draw_header(screen, "Memory Lane", "Answer together and see how well you remember your story")
        self.back_button.draw(screen, self.body_font)

        question = self.state.active_question()
        if question is None:
            self.draw_text(screen, "No memory questions yet. Add more in data/questions.json.", self.body_font, MUTED, SCREEN_WIDTH // 2, 360, center=True)
            return

        card = Card(
            rect=self.animate_rect(pygame.Rect(180, 190, 920, 150), delay=0.05),
            title=f"Question {self.state.current_question_index + 1}",
            body=question.prompt,
        )
        card.draw(screen, self.title_font, self.body_font)

        for button in self.option_buttons:
            button.draw(screen, self.body_font)

        self.draw_text(screen, f"Score: {self.state.score}", self.body_font, TEXT, 980, 60)
        self.draw_text(screen, f"Hearts: {self.state.hearts}", self.body_font, MUTED, 980, 92)
        self.finish_frame(screen)
