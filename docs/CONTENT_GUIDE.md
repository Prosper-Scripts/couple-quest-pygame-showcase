# Fictional Content Guide

The public repository intentionally contains **invented** relationship data, not a real couple's story. These JSON files are for demonstrating data-driven gameplay.

## Files and key fields

| File | Required data |
| --- | --- |
| `couple_profile.json` | `title`, `partner_one`, `partner_two`, `years_together`, `tagline`, `anniversary`, `home_message` |
| `memories.json` | A list of `id`, `title`, `year`, `location`, `description`; optional `date`, `tags`, `photo` |
| `questions.json` | A list of `id`, `category`, `prompt`; optional `answer`, `options`, `related_memory_id` |
| `challenges.json` | A list of `id`, `title`, `prompt`, `reward_text` |

## Dates and categories

- Use full dates as `YYYY-MM-DD`, for example `2024-06-18`.
- The `year` field must match the year in `date`.
- The timeline automatically sorts events from earliest to latest, regardless of their order in the JSON file.
- Question categories: `memory_lane`, `who_said_it`, `deep_talk`, `couple_goals`, and `marriage_talk`.
- Every `memory_lane` question needs at least two options with exactly one matching the `answer` (case-insensitive).
- Every `who_said_it` answer must match one of the two partner names in the profile.
- `related_memory_id`, when supplied, must point to a memory in `memories.json`.
- IDs must be unique within each respective data file.

Run the tests after changing examples:

```bash
python -m unittest discover -s tests -v
```

## Keep real-life content private

**Do not put real names, private dates, personal photos, relationship details or private conversations in this public GitHub repository.** Git repositories preserve earlier commits. If you want to build a personalized edition, use a separate local **private** project and review every file before sharing it. Simply adding an already-tracked file to `.gitignore` will not stop Git from tracking that file.
