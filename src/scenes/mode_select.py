import pygame

from config import MUTED, TEXT
from scenes.base import BaseScene
from ui.buttons import Button


class ModeSelectScene(BaseScene):
    def __init__(self, state) -> None:
        super().__init__(state)
        self.memory_button = Button("Memory Lane", pygame.Rect(220, 240, 360, 100))
        self.timeline_button = Button("Timeline Challenge", pygame.Rect(700, 240, 360, 100))
        self.quote_button = Button("Who Said It?", pygame.Rect(220, 390, 360, 100))
        self.mission_button = Button("Love Missions", pygame.Rect(700, 390, 360, 100))
        self.heart_talk_button = Button("Heart Talk", pygame.Rect(460, 540, 360, 100))
        self.back_button = Button("Back", pygame.Rect(60, 50, 120, 48), subtle=True)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.back_button.handle_event(event):
            self.play_sound("click")
            self.next_scene = "menu"
            return

        if self.memory_button.handle_event(event):
            self.play_sound("click")
            self.state.reset_mode("memory_lane")
            self.next_scene = "memory_lane"
        elif self.timeline_button.handle_event(event):
            self.play_sound("click")
            self.state.reset_mode("timeline")
            self.next_scene = "timeline"
        elif self.quote_button.handle_event(event):
            self.play_sound("click")
            self.state.reset_mode("who_said_it")
            self.next_scene = "who_said_it"
        elif self.mission_button.handle_event(event):
            self.play_sound("click")
            self.state.reset_mode("love_missions")
            self.next_scene = "love_missions"
        elif self.heart_talk_button.handle_event(event):
            self.play_sound("click")
            self.state.reset_mode("heart_talk")
            self.next_scene = "heart_talk"

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        self.draw_header(screen, "Pick Tonight's Mood", "Choose a mode and relive your story together")
        self.memory_button.draw(screen, self.body_font)
        self.timeline_button.draw(screen, self.body_font)
        self.quote_button.draw(screen, self.body_font)
        self.mission_button.draw(screen, self.body_font)
        self.heart_talk_button.draw(screen, self.body_font)
        self.back_button.draw(screen, self.body_font)
        self.draw_text(screen, "Five ways to explore a fictional shared story.", self.small_font, MUTED, 420, 665)
        self.finish_frame(screen)
