# Python Text Adventure Engine

A Zork-like text adventure engine in Python, designed for easy creation of new adventures by separating engine logic from game content.

## Project Structure

- `game_engine/` — Core engine code
  - `engine.py` — Main engine logic (handles game state, verbs, puzzles, dynamic room updates)
  - `version.py` — Engine version (semantic versioning)
- `adventure.py` — Click entry point for running a game
- `games/` — Game content files (JSON format)
- `.github/copilot-instructions.md` — Project automation and setup checklist

## Features

- Movement between locations (e.g., `north`, `n`, `south`, `s`, etc.)
- Inventory management (`get`, `take`, `grab`, `drop`, `inventory`, `i`)
- Use and place items (`use`, `place`, `put`)
- Puzzle system: define puzzles in the game file, solved by `use` or `place` actions
- Post-puzzle actions: reveal new exits, add/remove items, print messages, etc.
- Dynamic room descriptions: new exits and items are described after puzzles
- Command aliases and natural language parsing (e.g., `place the key in the chest`)
- In-game help (`help`, `h`)
- Scoring system: earn points for solving puzzles (see `score` field in puzzles)
- Move tracking: see how many moves you've made (`moves` command, shown at game end)
- Save/Load: save your progress to a file and load it later (`save`, `load`)
- Engine and content are fully separated
- Semantic versioning and proper git version control

## How to Run

1. Make sure you have Python 3 and Click installed (or use the provided `.venv`).
2. From the project root, run:

   ```bash
   adventure games/haunted_mansion.json
   ```

   Or, if not installed as a CLI:
   ```bash
   python adventure.py games/haunted_mansion.json
   ```

## Creating a Game File

Game files are written in JSON. Example (see `games/haunted_mansion.json`):

```json
{
    "start_location": "Foyer",
    "locations": {
        "Foyer": {
            "description": "You are in the dusty foyer of a spooky old mansion. A grand staircase leads up, but it's blocked by rubble. A single door stands to the north.",
            "exits": { "north": "Library" },
            "items": ["key"]
        },
        "Library": {
            "description": "You've entered a musty library lined with shelves of ancient, decaying books. In the center of the room sits a large, locked chest. A door leads south.",
            "exits": { "south": "Foyer" }
        },
        "Secret Room": {
            "description": "A hidden room filled with cobwebs and a pile of treasure! The only exit is west back to the Library.",
            "exits": { "west": "Library" },
            "items": []
        }
    },
    "puzzles": [
        {
            "type": "place",
            "item": "key",
            "target": "chest",
            "location": "Library",
            "success": "You place the key in the lock and turn it. The chest clicks open!",
            "remove_item": true,
            "score": 10,
            "actions": [
                {"type": "add_item", "location": "Library", "item": "treasure"},
                {"type": "add_exit", "location": "Library", "direction": "east", "to": "Secret Room"},
                {"type": "print", "message": "A secret door slides open to the east!"}
            ]
        }
    ]
}
```

- Movement: `north`, `n`, `south`, `s`, `east`, `e`, `west`, `w`, `up`, `u`, `down`, `d`
- `look`, `l` — Look around
- `get`, `take`, `grab <item>` — Pick up an item
- `drop <item>` — Drop an item
- `inventory`, `i` — Show your inventory
- `use <item>` — Use an item (triggers puzzles if defined)
- `place`, `put <item> <target>` — Place an item (triggers puzzles if defined)
- `score` — Show your current score
- `moves` — Show how many moves you've made
- `save` — Save your game progress
- `load` — Load a saved game
- `help`, `h` — Show help
- `quit`, `exit` — Exit the game

## Natural Language Parsing

- Filler words like "the", "in", "on", "at", etc. are ignored, so you can type commands like `place the key in the chest`.

## Extending the Engine

- Add new verbs or puzzle types by editing `game_engine/engine.py`.
- Add new locations, items, and puzzles by editing or creating new JSON files in `games/`.

## Versioning

- Engine version is tracked in `game_engine/version.py` and `setup.py`.
- All changes are committed to git with semantic versioning (MAJOR.MINOR.PATCH).

## License

MIT License
