import json
import os

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []

    def add_exit(self, direction, location_name):
        self.exits[direction] = location_name

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)


DIRECTION_ALIASES = {
    'n': 'north', 's': 'south', 'e': 'east', 'w': 'west',
    'u': 'up', 'd': 'down',
    'north': 'north', 'south': 'south', 'east': 'east', 'west': 'west',
    'up': 'up', 'down': 'down'
}
ACTION_ALIASES = {
    'get': 'get', 'take': 'get', 'grab': 'get',
    'drop': 'drop',
    'inventory': 'inventory', 'i': 'inventory',
    'look': 'look', 'l': 'look',
    'use': 'use',
    'place': 'place', 'put': 'place',
    'quit': 'quit', 'exit': 'quit',
    'help': 'help', 'h': 'help',
    'score': 'score',
    'moves': 'moves',
    'save': 'save',
    'load': 'load'
}

HELP_TEXT = '''
Available commands:
    n,s,e,w,u,d      Move north, south, east, west, up, down
    look, l          Look around
    get/take/grab    Pick up an item (e.g. get key)
    drop             Drop an item (e.g. drop key)
    use              Use an item (e.g. use key)
    place/put        Place an item (e.g. place key chest)
    inventory, i     Show your inventory
    score            Show your current score
    moves            Show how many moves you've made
    save             Save your game
    load             Load your game
    help, h          Show this help message
    quit, exit       Quit the game
'''

FILLER_WORDS = {"the", "a", "an", "in", "on", "at", "to", "with", "and", "of", "from", "into", "onto", "upon"}


class GameEngine:
    def __init__(self):
        self.locations = {}
        self.current_location = None
        self.inventory = []
        self.puzzles = []
        self.ended = False
        self.end_summary = None
        self.score = 0
        self.moves = 0
        self._gamefile = None

    def load_game(self, file_path):
        self._gamefile = file_path
        with open(file_path, 'r') as f:
            game_data = json.load(f)
        
        self.locations = {} # Clear previous locations
        for loc_name, loc_data in game_data['locations'].items():
            location = Location(loc_name, loc_data['description'])
            for item in loc_data.get('items', []):
                location.add_item(item)
            for direction, dest_name in loc_data.get('exits', {}).items():
                location.add_exit(direction, dest_name)
            self.add_location(location)
        
        self.set_current_location(game_data['start_location'])
        self.puzzles = game_data.get('puzzles', [])
        # Reset game state variables that shouldn't persist across game loads
        self.inventory = []
        self.score = 0
        self.moves = 0
        self.ended = False
        self.end_summary = None


    def add_location(self, location):
        self.locations[location.name] = location

    def set_current_location(self, location_name):
        self.current_location = self.locations.get(location_name)

    def play(self):
        if not self.current_location:
            print("No starting location set.")
            return
        while not self.ended:
            print()
            self.print_location_description()
            if self.current_location.items:
                print("You see:", ", ".join(self.current_location.items))
            
            command = input("> ").strip().lower().split()
            if not command:
                continue
            
            action_word = command[0]
            args = [w for w in command[1:] if w not in FILLER_WORDS]

            if action_word in DIRECTION_ALIASES:
                dir_full = DIRECTION_ALIASES[action_word]
                if dir_full in self.current_location.exits:
                    self.set_current_location(self.current_location.exits[dir_full])
                    self.moves += 1
                else:
                    print("You can't go that way.")
                continue

            action = ACTION_ALIASES.get(action_word)

            if action == "look":
                continue
            elif action == "help":
                print(HELP_TEXT)
            elif action == "score":
                print(f"Your score is {self.score}.")
            elif action == "moves":
                print(f"You have made {self.moves} moves.")
            elif action == "save":
                self.save_game()
            elif action == "load":
                self.load_saved_game()
            elif action == "quit":
                print("Thanks for playing!")
                self.ended = True
            elif action == "get" and args:
                item = args[0]
                if item in self.current_location.items:
                    self.current_location.remove_item(item)
                    self.inventory.append(item)
                    print(f"You picked up the {item}.")
                    self.moves += 1
                else:
                    print("You don't see that here.")
            elif action == "drop" and args:
                item = args[0]
                if item in self.inventory:
                    self.inventory.remove(item)
                    self.current_location.add_item(item)
                    print(f"You dropped the {item}.")
                    self.moves += 1
                else:
                    print("You don't have that.")
            elif action == "inventory":
                if self.inventory:
                    print("You are carrying:", ", ".join(self.inventory))
                else:
                    print("Your inventory is empty.")
            elif action == "use" and args:
                item = args[0]
                self.handle_use(item)
                self.moves += 1
            elif action == "place" and len(args) >= 2:
                item = args[0]
                target = " ".join(args[1:])
                self.handle_place(item, target)
                self.moves += 1
            else:
                print("I don't understand that command. Type 'help' for a list of commands.")

        if self.ended and self.end_summary:
             print("\n=== GAME OVER ===")
             print(self.end_summary)
             print(f"Your final score is {self.score}.")
             print(f"You made {self.moves} moves.")

    def print_location_description(self):
        if not self.current_location:
            return
        desc = self.current_location.description
        exits = list(self.current_location.exits.keys())
        desc += "\nExits: " + ", ".join(exits)
        print(desc)

    def handle_use(self, item):
        if item not in self.inventory:
            print(f"You don't have a {item} to use.")
            return
        for puzzle in self.puzzles:
            if puzzle['type'] == 'use' and puzzle['item'] == item and (('location' not in puzzle) or puzzle['location'] == self.current_location.name):
                if puzzle.get('solved', False):
                    print(puzzle.get('already_solved_message', "You've already done that."))
                    return
                print(puzzle['success'])
                if puzzle.get('remove_item', False):
                    self.inventory.remove(item)
                self.handle_puzzle_actions(puzzle)
                if 'score' in puzzle:
                    self.score += puzzle['score']
                    print(f"You gained {puzzle['score']} points! Your score is now {self.score}.")
                puzzle['solved'] = True # Mark as solved
                if puzzle.get('end_game'):
                    self.ended = True
                    self.end_summary = puzzle.get('end_summary', 'The game has ended.')
                return
        print(f"You try to use the {item}, but nothing happens.")

    def handle_place(self, item, target):
        if item not in self.inventory:
            print(f"You don't have a {item} to place.")
            return
        for puzzle in self.puzzles:
            if puzzle['type'] == 'place' and puzzle['item'] == item and puzzle['target'] == target and puzzle['location'] == self.current_location.name:
                if puzzle.get('solved', False):
                    print(puzzle.get('already_solved_message', "You've already done that."))
                    return
                print(puzzle['success'])
                if puzzle.get('remove_item', False):
                    self.inventory.remove(item)
                self.handle_puzzle_actions(puzzle)
                if 'score' in puzzle:
                    self.score += puzzle['score']
                    print(f"You gained {puzzle['score']} points! Your score is now {self.score}.")
                puzzle['solved'] = True # Mark as solved
                if puzzle.get('end_game'):
                    self.ended = True
                    self.end_summary = puzzle.get('end_summary', 'The game has ended.')
                return
        print(f"You try to place the {item} on the {target}, but nothing happens.")

    def handle_puzzle_actions(self, puzzle):
        actions = puzzle.get('actions', [])
        for act in actions:
            if act['type'] == 'add_exit':
                loc = self.locations.get(act['location'])
                if loc:
                    loc.add_exit(act['direction'], act['to'])
            elif act['type'] == 'remove_exit':
                loc = self.locations.get(act['location'])
                if loc and act['direction'] in loc.exits:
                    del loc.exits[act['direction']]
            elif act['type'] == 'add_item':
                loc = self.locations.get(act['location'])
                if loc:
                    loc.add_item(act['item'])
            elif act['type'] == 'remove_item':
                loc = self.locations.get(act['location'])
                if loc and act['item'] in loc.items:
                    loc.remove_item(act['item'])
            elif act['type'] == 'print':
                print(act['message'])

    def save_game(self):
        save_dir = "savegames"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        if not self._gamefile:
            print("Cannot determine original game file name for save.")
            return
        
        base_name = os.path.basename(self._gamefile)
        save_filename = os.path.splitext(base_name)[0] + "_savegame.json"
        save_path = os.path.join(save_dir, save_filename)

        # Collect puzzle solved states
        puzzle_states = [p.get('solved', False) for p in self.puzzles]

        state = {
            "original_gamefile": self._gamefile,
            "current_location": self.current_location.name if self.current_location else None,
            "inventory": self.inventory,
            "score": self.score,
            "moves": self.moves,
            "locations": {name: {"items": loc.items.copy(), "exits": loc.exits.copy()} for name, loc in self.locations.items()},
            "puzzle_states": puzzle_states
        }
        try:
            with open(save_path, 'w') as f:
                json.dump(state, f, indent=4)
            print(f"Game saved to {save_path}.")
        except Exception as e:
            print(f"Failed to save game: {e}")

    def load_saved_game(self):
        save_dir = "savegames"
        if not self._gamefile:
            print("Cannot determine original game file name for load.")
            return

        base_name = os.path.basename(self._gamefile)
        save_filename = os.path.splitext(base_name)[0] + "_savegame.json"
        save_path = os.path.join(save_dir, save_filename)

        if not os.path.exists(save_path):
            print(f"No save file found at {save_path}.")
            return

        try:
            with open(save_path, 'r') as f:
                state = json.load(f)
            
            # Reload the original game to reset the base state
            self.load_game(state["original_gamefile"])

            # Restore the saved state
            self.set_current_location(state["current_location"])
            self.inventory = state["inventory"]
            self.score = state["score"]
            self.moves = state["moves"]
            
            # Restore dynamic location state (items/exits)
            if "locations" in state:
                for name, loc_state in state["locations"].items():
                    if name in self.locations:
                        self.locations[name].items = loc_state.get("items", [])
                        self.locations[name].exits = loc_state.get("exits", {})
            
            # Restore puzzle solved states
            if "puzzle_states" in state:
                for i, solved in enumerate(state["puzzle_states"]):
                    if i < len(self.puzzles):
                        self.puzzles[i]['solved'] = solved

            print(f"Game loaded from {save_path}.")
            # Reprint location after loading
            self.print_location_description()
            if self.current_location and self.current_location.items:
                print("You see:", ", ".join(self.current_location.items))

        except Exception as e:
            print(f"Failed to load game: {e}")
