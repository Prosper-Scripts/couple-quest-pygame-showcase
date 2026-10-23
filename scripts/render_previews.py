"""Render sample screens with a headless SDL driver for portfolio screenshots.

Run after installing requirements: python scripts/render_previews.py
This checks that every scene can draw one frame; it does not simulate clicks.
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pygame

from main import GameApp, SCENE_REGISTRY


def main() -> None:
    app = GameApp()
    previews = ROOT / "assets" / "images"
    previews.mkdir(parents=True, exist_ok=True)

    scene_modes = {
        "memory_lane": "memory_lane",
        "timeline": "timeline",
        "who_said_it": "who_said_it",
        "love_missions": "love_missions",
        "heart_talk": "heart_talk",
    }
    try:
        for scene_name, scene_class in SCENE_REGISTRY.items():
            if scene_name in scene_modes:
                app.state.reset_mode(scene_modes[scene_name])
            scene = scene_class(app.state)
            scene.entered_at -= 1.0  # Hide the entry animation in static captures.
            scene.render(app.screen)
            if scene_name in ("menu", "mode_select", "timeline"):
                pygame.image.save(app.screen, str(previews / f"{scene_name}.png"))
            print(f"Rendered {scene_name}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
