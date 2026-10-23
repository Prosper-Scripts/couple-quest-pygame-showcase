# Architecture

## Design goals

Couple Quest separates data, rules and drawing so gameplay can be tested without initializing a display. The demo uses local JSON and procedural audio; there is no database, network request or account service.

## Module responsibilities

| Module | Responsibility |
| --- | --- |
| `src/main.py` | Initialize Pygame; own event loop, scene registry, rendering and input mapping |
| `src/config.py` | Screen dimensions, color palette, paths and sound levels |
| `src/game/models.py` | Typed dataclasses for profiles, events, questions, missions and content |
| `src/game/loader.py` | Deserialize JSON into dataclasses and validate the result |
| `src/game/validation.py` | Reject invalid dates, duplicate IDs, broken memory links and answer mismatches |
| `src/game/timeline.py` | Deterministically compare memory dates without relying on JSON order |
| `src/game/state.py` | Reset modes, select decks, track score/hearts and expose active items |
| `src/game/scoring.py` | Pure multiple-choice answer comparison |
| `src/game/audio.py` | Procedurally synthesize short effects and an ambient loop; play with Pygame mixer |
| `src/scenes/` | One view/controller per gameplay mode plus menu and results |
| `src/ui/` | Shared buttons, cards and drawing/theme helpers |

## Round lifecycle

1. `GameApp` loads the fictional content and instantiates `GameState`.
2. The mode-selection scene calls `GameState.reset_mode(mode)`.
3. The active scene renders questions or events from the session state.
4. Mouse events are translated from displayed pixels to the 1280 × 720 logical canvas and dispatched to the active scene.
5. Answers update score, hearts, session notes and progression; the results scene summarizes the round.

Timeline Challenge samples up to four memories, sorts them by `datetime.date`, and displays only **unsolved** memories as options. `date` must use ISO `YYYY-MM-DD` format when present. Events missing a day have a clearly defined year-only fallback of January 1; for precise ordering, supply full dates.

## Quality boundaries

All tests under `tests/` import core game modules, but not `pygame`. They therefore run in CI, minimal Python environments, and headless systems without an installed display. Rendering, sound playback and pointer input require a separate graphical smoke test.

The current window defaults to 1280 × 720. Fullscreen mode letterboxes/scales the logical canvas while preserving pointer hit-testing. Live resizing of the window is not yet implemented.

## Trade-offs and future extensions

- JSON makes prototypes easy to edit, but a content editor should validate and preview user submissions.
- `GameState` owns one round at a time; persistence would be a separate repository/service concern.
- Data checks run when content is loaded, failing early with descriptive errors.
- Sound is generated locally, avoiding externally licensed music assets.
- A full accessibility pass would add keyboard navigation, focus indicators, caption toggles, and reduced-motion preferences.
