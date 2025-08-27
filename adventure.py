import click
from game_engine.engine import GameEngine

@click.command()
@click.argument('gamefile', type=click.Path(exists=True))
def adventure(gamefile):
    """Run a text adventure game from a JSON file."""
    engine = GameEngine()
    engine.load_game(gamefile)
    engine.play()

if __name__ == '__main__':
    adventure()
