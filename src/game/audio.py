import math
import struct
import wave
from pathlib import Path

import pygame

from config import ASSETS_DIR


SOUND_DIR = ASSETS_DIR / "sounds"
SAMPLE_RATE = 44100
CHANNEL_COUNT = 2
GENERATION_VERSION = "romantic-v1"

AudioEvent = tuple[float, float, tuple[float, ...], float, float, str]


def midi_to_freq(note: int) -> float:
    return 440.0 * (2 ** ((note - 69) / 12))


def _waveform_value(waveform: str, frequency: float, t: float) -> float:
    phase = 2 * math.pi * frequency * t
    sine = math.sin(phase)

    if waveform == "triangle":
        return (2 / math.pi) * math.asin(sine)
    if waveform == "bell":
        overtone = math.sin(phase * 2) * 0.35
        shimmer = math.sin(phase * 3) * 0.18
        return (sine * 0.82) + overtone + shimmer
    if waveform == "soft_square":
        return math.tanh(sine * 2.4)
    return sine


def _event_envelope(progress: float) -> float:
    if progress <= 0.12:
        return progress / 0.12
    if progress >= 0.82:
        return max(0.0, (1 - progress) / 0.18)
    return 1.0


def _render_events(events: list[AudioEvent], total_duration: float) -> bytes:
    total_frames = max(1, int(SAMPLE_RATE * total_duration))
    left = [0.0] * total_frames
    right = [0.0] * total_frames

    for start, duration, frequencies, volume, pan, waveform in events:
        start_frame = int(start * SAMPLE_RATE)
        frame_count = max(1, int(duration * SAMPLE_RATE))
        left_gain = (1 - pan) * 0.5
        right_gain = (1 + pan) * 0.5

        for frame_offset in range(frame_count):
            frame_index = start_frame + frame_offset
            if frame_index >= total_frames:
                break

            t = frame_offset / SAMPLE_RATE
            progress = frame_offset / frame_count
            envelope = _event_envelope(progress)

            sample_value = 0.0
            for frequency in frequencies:
                sample_value += _waveform_value(waveform, frequency, t)
            sample_value /= max(1, len(frequencies))
            sample_value *= volume * envelope

            left[frame_index] += sample_value * left_gain
            right[frame_index] += sample_value * right_gain

    frames: list[bytes] = []
    for frame_index in range(total_frames):
        left_value = max(-1.0, min(1.0, left[frame_index]))
        right_value = max(-1.0, min(1.0, right[frame_index]))
        frames.append(struct.pack("<hh", int(left_value * 32767), int(right_value * 32767)))
    return b"".join(frames)


def _write_wave_file(path: Path, events: list[AudioEvent], total_duration: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(CHANNEL_COUNT)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(_render_events(events, total_duration))


def _sequential_events(steps: list[tuple[tuple[int, ...], float, float, float, str]]) -> tuple[list[AudioEvent], float]:
    events: list[AudioEvent] = []
    cursor = 0.0

    for midi_notes, duration, volume, pan, waveform in steps:
        frequencies = tuple(midi_to_freq(note) for note in midi_notes)
        events.append((cursor, duration, frequencies, volume, pan, waveform))
        cursor += duration

    return events, cursor


def _build_ambience_events() -> tuple[list[AudioEvent], float]:
    bar = 1.6
    progression = [
        ((48, 60, 64, 67), (72, 76, 79)),
        ((43, 55, 59, 62), (71, 74, 79)),
        ((45, 57, 60, 64), (69, 72, 76)),
        ((41, 53, 57, 60), (69, 72, 77)),
        ((48, 60, 64, 67), (72, 76, 79)),
        ((45, 57, 60, 64), (69, 72, 76)),
        ((43, 55, 59, 62), (67, 71, 74)),
        ((41, 53, 57, 60), (69, 72, 76)),
    ]

    events: list[AudioEvent] = []
    total_duration = len(progression) * bar

    for index, (pad_notes, sparkle_notes) in enumerate(progression):
        start = index * bar
        pad_freqs = tuple(midi_to_freq(note) for note in pad_notes)
        sparkle_freqs = tuple(midi_to_freq(note) for note in sparkle_notes)
        bass_freq = (midi_to_freq(pad_notes[0]),)

        events.append((start, bar * 1.05, pad_freqs, 0.12, -0.12, "triangle"))
        events.append((start, bar * 0.86, bass_freq, 0.11, 0.0, "sine"))

        for pulse in range(4):
            pulse_start = start + (pulse * 0.34) + 0.06
            note = (sparkle_freqs[pulse % len(sparkle_freqs)],)
            pan = -0.28 if pulse % 2 == 0 else 0.28
            events.append((pulse_start, 0.22, note, 0.08, pan, "bell"))

    return events, total_duration


def ensure_default_sounds() -> None:
    version_file = SOUND_DIR / ".generated_version"

    sound_recipes = {
        "start.wav": _sequential_events(
            [
                ((60, 64, 67), 0.14, 0.26, -0.10, "bell"),
                ((64, 67, 72), 0.18, 0.30, 0.10, "bell"),
                ((67, 72, 76), 0.28, 0.34, 0.0, "bell"),
            ]
        ),
        "click.wav": _sequential_events(
            [
                ((74, 81), 0.07, 0.18, 0.12, "bell"),
            ]
        ),
        "correct.wav": _sequential_events(
            [
                ((64, 67), 0.10, 0.23, -0.16, "bell"),
                ((67, 72), 0.11, 0.26, 0.0, "bell"),
                ((72, 76, 79), 0.22, 0.30, 0.14, "bell"),
            ]
        ),
        "wrong.wav": _sequential_events(
            [
                ((64, 67), 0.10, 0.20, 0.06, "soft_square"),
                ((60, 63), 0.12, 0.20, -0.04, "soft_square"),
                ((57,), 0.24, 0.18, 0.0, "triangle"),
            ]
        ),
        "transition.wav": _sequential_events(
            [
                ((67,), 0.08, 0.14, -0.16, "bell"),
                ((71,), 0.10, 0.15, 0.16, "bell"),
                ((74,), 0.14, 0.16, 0.0, "bell"),
            ]
        ),
        "win.wav": _sequential_events(
            [
                ((67, 71), 0.12, 0.24, -0.10, "bell"),
                ((72, 76), 0.15, 0.28, 0.10, "bell"),
                ((76, 79, 83), 0.34, 0.32, 0.0, "bell"),
            ]
        ),
        "ambience.wav": _build_ambience_events(),
    }

    expected_files = [SOUND_DIR / filename for filename in sound_recipes]
    version_matches = version_file.exists() and version_file.read_text(encoding="utf-8").strip() == GENERATION_VERSION
    files_exist = all(path.exists() for path in expected_files)

    if version_matches and files_exist:
        return

    SOUND_DIR.mkdir(parents=True, exist_ok=True)
    for filename, (events, total_duration) in sound_recipes.items():
        _write_wave_file(SOUND_DIR / filename, events, total_duration)

    version_file.write_text(GENERATION_VERSION, encoding="utf-8")


class AudioManager:
    def __init__(self, sfx_volume: float = 0.45, music_volume: float = 0.22) -> None:
        self.enabled = False
        self.sounds: dict[str, pygame.mixer.Sound] = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            ensure_default_sounds()
            for name in ("start", "click", "correct", "wrong", "transition", "win"):
                sound = pygame.mixer.Sound(str(SOUND_DIR / f"{name}.wav"))
                sound.set_volume(sfx_volume)
                self.sounds[name] = sound

            pygame.mixer.music.load(str(SOUND_DIR / "ambience.wav"))
            pygame.mixer.music.set_volume(music_volume)
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def play(self, name: str) -> None:
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    def start_music(self) -> None:
        if self.enabled and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1, fade_ms=900)

    def stop_music(self) -> None:
        if self.enabled:
            pygame.mixer.music.fadeout(600)
