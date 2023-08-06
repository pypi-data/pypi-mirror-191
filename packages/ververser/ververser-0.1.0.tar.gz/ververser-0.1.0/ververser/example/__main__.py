import logging
from pathlib import Path
from game_window import GameWindow


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    game = GameWindow(
        asset_folder_path = Path( __file__ ).parent / 'content'
    )
    game.run()
