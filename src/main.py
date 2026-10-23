import sys

import pygame

from config import AUDIO_VOLUME, FPS, FULLSCREEN, MUSIC_VOLUME, SCREEN_HEIGHT, SCREEN_WIDTH, WINDOW_TITLE
from game.audio import AudioManager
from game.loader import load_game_content
from game.state import GameState
from scenes.love_missions import LoveMissionsScene
from scenes.memory_lane import MemoryLaneScene
from scenes.menu import MenuScene
from scenes.mode_select import ModeSelectScene
from scenes.results import ResultsScene
from scenes.splash import SplashScene
from scenes.heart_talk import HeartTalkScene
from scenes.timeline import TimelineScene
from scenes.who_said_it import WhoSaidItScene


SCENE_REGISTRY = {
    "splash": SplashScene,
    "menu": MenuScene,
    "mode_select": ModeSelectScene,
    "memory_lane": MemoryLaneScene,
    "timeline": TimelineScene,
    "who_said_it": WhoSaidItScene,
    "love_missions": LoveMissionsScene,
    "heart_talk": HeartTalkScene,
    "results": ResultsScene,
}


class GameApp:
    def __init__(self) -> None:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        display_flags = pygame.FULLSCREEN if FULLSCREEN else 0
        display_size = (0, 0) if FULLSCREEN else (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.display = pygame.display.set_mode(display_size, display_flags)
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.render_rect = self._compute_render_rect()
        self.clock = pygame.time.Clock()
        self.content = load_game_content()
        self.state = GameState(self.content)
        self.state.audio = AudioManager(AUDIO_VOLUME, MUSIC_VOLUME)
        self.scene = SplashScene(self.state)
        if self.state.audio is not None:
            self.state.audio.start_music()
            self.state.audio.play("start")

    def change_scene(self, scene_name: str) -> None:
        scene_class = SCENE_REGISTRY[scene_name]
        self.scene = scene_class(self.state)
        if self.state.audio is not None:
            self.state.audio.play("win" if scene_name == "results" else "transition")

    def _compute_render_rect(self) -> pygame.Rect:
        display_width, display_height = self.display.get_size()
        scale = min(display_width / SCREEN_WIDTH, display_height / SCREEN_HEIGHT)
        width = int(SCREEN_WIDTH * scale)
        height = int(SCREEN_HEIGHT * scale)
        x = (display_width - width) // 2
        y = (display_height - height) // 2
        return pygame.Rect(x, y, width, height)

    def _translate_mouse_event(self, event: pygame.event.Event) -> pygame.event.Event:
        event_data = event.dict.copy()
        event_pos = event_data.get("pos")
        if event_pos is None:
            return event

        translated_pos = self._translate_pos(event_pos)
        if translated_pos is None:
            event_data["pos"] = (-9999, -9999)
        else:
            event_data["pos"] = translated_pos
        return pygame.event.Event(event.type, event_data)

    def _translate_pos(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        if not self.render_rect.collidepoint(pos):
            return None

        local_x = (pos[0] - self.render_rect.x) / self.render_rect.width
        local_y = (pos[1] - self.render_rect.y) / self.render_rect.height
        return (int(local_x * SCREEN_WIDTH), int(local_y * SCREEN_HEIGHT))

    def _present(self) -> None:
        scaled = pygame.transform.smoothscale(self.screen, self.render_rect.size)
        self.display.fill((0, 0, 0))
        self.display.blit(scaled, self.render_rect)
        pygame.display.flip()

    def run(self) -> None:
        while self.scene.is_running:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.scene.is_running = False
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.scene.is_running = False
                    break
                if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    event = self._translate_mouse_event(event)
                self.scene.handle_event(event)

            self.state.update(dt)
            self.scene.update(dt)
            self.scene.render(self.screen)
            self._present()

            if self.scene.next_scene is not None:
                self.change_scene(self.scene.next_scene)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    GameApp().run()
