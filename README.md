# Python Text Adventure Engine

A Zork-like text adventure engine in Python, designed for easy creation of new adventures by separating engine logic from game content.

## Project Structure

- `game_engine/` — Core engine code
  - `engine.py` — Main engine logic (handles game state, verbs, puzzles)
  - `main.py` — Entry point for running a game
- `games/` — Game content files (JSON format)

## Features

- Movement between locations (e.g., `north`, `south`, etc.)
- Inventory management (`get`, `drop`, `inventory`)
- Use and place items (`use flashlight`, `place coins on altar`)
- Puzzle system: define puzzles in the game file, solved by `use` or `place` actions
- Engine and content are fully separated

## How to Run

1. Make sure you have Python 3 installed.
2. From the project root, run:

   ```bash
   python3 -m game_engine.main games/sample_game.json
   ```

   Replace `sample_game.json` with your own game file if desired.

## Creating a Game File

Game files are written in JSON. Example:

```json
{
    "start_location": "Cave Entrance",
    "locations": {
        "Cave Entrance": {
            "description": "You stand at the entrance of a dark cave. A path leads north into the darkness.",
            "exits": { "north": "Dark Chamber" },
            "items": ["flashlight"]
        },
        "Dark Chamber": {
            "description": "A pitch-black chamber. You can barely see. There is an altar here.",
            "exits": { "south": "Cave Entrance" },
            "items": ["coins"]
        }
    },
    "puzzles": [
        {
            "type": "use",
            "item": "flashlight",
            "location": "Dark Chamber",
            "success": "You turn on the flashlight and the chamber is illuminated! You see an ancient altar.",
            "remove_item": false
        },
        {
            "type": "place",
            "item": "coins",
            "target": "altar",
            "location": "Dark Chamber",
            "success": "You place the coins on the altar. A secret passage opens!",
            "remove_item": true
        }
    ]
}
```

## Supported Verbs

- Movement: `north`, `south`, `east`, `west`, etc.
- `get <item>` — Pick up an item
- `drop <item>` — Drop an item
- `inventory` — Show your inventory
- `use <item>` — Use an item (triggers puzzles if defined)
- `place <item> [on] <target>` — Place an item on a target (triggers puzzles if defined)
- `quit` — Exit the game

## Extending the Engine

- Add new verbs or puzzle types by editing `game_engine/engine.py`.
- Add new locations, items, and puzzles by editing or creating new JSON files in `games/`.

## License

MIT License
