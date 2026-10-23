import random

import pygame

from config import MUTED, TEXT
from scenes.base import BaseScene
from ui.buttons import Button
from ui.cards import Card


class TimelineScene(BaseScene):
    def __init__(self, state) -> None:
        super().__init__(state)
        self.back_button = Button("Back", pygame.Rect(60, 50, 120, 48), subtle=True)
        self.option_buttons = []
        self._build_option_buttons()

    def _build_option_buttons(self) -> None:
        self.option_buttons = []
        memories = self.state.remaining_timeline_memories()
        shuffled = memories[:]
        random.shuffle(shuffled)

        start_y = 350
        for index, memory in enumerate(shuffled):
            rect = pygame.Rect(220, start_y + (index * 72), 840, 56)
            self.option_buttons.append((memory.id, Button(memory.title, rect)))

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.back_button.handle_event(event):
            self.play_sound("click")
            self.next_scene = "mode_select"
            return

        target_memory = self.state.active_timeline_memory()
        if target_memory is None:
            self.next_scene = "results"
            return

        for memory_id, button in self.option_buttons:
            if button.handle_event(event):
                if memory_id == target_memory.id:
                    self.play_sound("correct")
                    self.show_feedback("Timeline locked in.", "success")
                    self.state.score += 1
                    self.state.add_result(f"Timeline Challenge: You placed '{target_memory.title}' in the right spot.")
                    self.state.current_question_index += 1
                    if self.state.current_question_index >= len(self.state.session_memories):
                        self.next_scene = "results"
                    else:
                        self._build_option_buttons()
                else:
                    self.play_sound("wrong")
                    self.show_feedback("That happened later.", "warning")
                    self.state.hearts -= 1
                    self.state.add_result(f"Timeline Challenge: You missed the next event after '{target_memory.title}'.")
                    if self.state.hearts <= 0:
                        self.next_scene = "results"
                break

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        self.draw_header(screen, "Timeline Challenge", "Choose the earliest remaining event until your relationship timeline is complete")
        self.back_button.draw(screen, self.body_font)

        current_memory = self.state.active_timeline_memory()
        if current_memory is None:
            self.draw_text(screen, "No timeline memories yet. Add more in data/memories.json.", self.body_font, MUTED, 350, 360)
            return

        card = Card(
            rect=self.animate_rect(pygame.Rect(170, 190, 940, 110), delay=0.05),
            title=f"Pick Event {self.state.current_question_index + 1}",
            body="Tap the memory that happened earliest among the choices below.",
        )
        card.draw(screen, self.subtitle_font, self.body_font)

        for _, button in self.option_buttons:
            button.draw(screen, self.body_font)

        if self.state.current_question_index > 0:
            previous = self.state.session_memories[self.state.current_question_index - 1]
            previous_label = previous.date or str(previous.year)
            self.draw_text(screen, f"Last correct event: {previous.title} ({previous_label})", self.body_font, TEXT, 220, 650)
        else:
            self.draw_text(screen, "Start with the earliest memory you see.", self.body_font, TEXT, 220, 650)

        self.draw_text(screen, f"Score: {self.state.score} | Hearts: {self.state.hearts}", self.body_font, MUTED, 860, 650)
        self.finish_frame(screen)
