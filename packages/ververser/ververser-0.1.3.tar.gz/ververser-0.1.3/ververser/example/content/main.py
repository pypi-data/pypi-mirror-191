from typing import Optional

from ververser.game_window import GameWindow

from pyglet.gl import glClearColor

import random


def _r() -> float:
    return random.uniform(0, 1)

class Game:

    def __init__( self, game_window : GameWindow ):
        self.game_window = game_window

    def update( self, dt ):
        glClearColor( _r(), 1, 1, 1.0 )

    def draw( self ):
        ...


# --------
# This is just some boilerplate that makes it easier to use a custom Game class

_GAME : Optional[ Game ] = None

def init( game_window : GameWindow ):
    global _GAME
    _GAME = Game( game_window )

def update( dt ):
    _GAME.update( dt )

def draw():
    _GAME.draw()