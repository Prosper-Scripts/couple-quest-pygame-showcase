from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
ASSETS_DIR = ROOT_DIR / "assets"
SAVES_DIR = ROOT_DIR / "saves"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Couple Quest | Interactive Pygame Demo"
FULLSCREEN = False
AUDIO_VOLUME = 0.45
MUSIC_VOLUME = 0.22

BACKGROUND = (248, 236, 229)
PANEL = (255, 250, 246)
PANEL_ALT = (243, 225, 216)
TEXT = (72, 43, 35)
MUTED = (125, 92, 84)
ACCENT = (201, 86, 111)
ACCENT_DARK = (146, 54, 78)
SUCCESS = (88, 145, 110)
WARNING = (214, 152, 87)
SHADOW = (210, 188, 180)

FONT_NAME = "georgia"
