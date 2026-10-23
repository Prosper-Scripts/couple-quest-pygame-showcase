# Portfolio Case Study — Couple Quest

## Problem

Create a small desktop experience that turns static story data into playful interactive activities while keeping game logic, presentation and content separate.

## Implementation

- **Data-driven modes:** Five independent Pygame scenes read typed profile, memory, quiz and mission models.
- **Stateful play:** A session controller manages mode-specific question samples, remaining hearts, points, round transitions and summaries.
- **Correct chronological logic:** A reusable pure function sorts ISO date values rather than trusting how data files happen to be arranged.
- **Consistent input:** The central event loop scales screen coordinates back into a logical 1280 × 720 canvas.
- **Modular UI:** Shared buttons and card components provide consistent interactions across game modes.
- **Procedural sound:** An in-project synth generates feedback sounds and looping ambience without third-party music assets.
- **Data validation:** The loader rejects inconsistent references, dates and quiz answers at startup.

## Verification

Run `python -m unittest discover -s tests -v` for reproducible tests that exercise content integrity, scoring, mode resets and timeline rules. The core tests are headless and do not require Pygame. Full graphical interaction and audio playback need separate runtime verification on a desktop machine.

## Scope and limitations

This is a demonstrable prototype, not a production matchmaking or social platform. It has no user accounts, cloud storage or data collection. No claims are made about deployment scale or measured performance. Personalization and persistent saves are possible follow-up features, not currently implemented.

The public edition uses fully fictional content. It exists as a shareable engineering demonstration separate from the private original project.
