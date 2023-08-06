from typing import Optional

from ververser.game_window import GameWindow

from pyglet.gl import glClearColor


class Game:

    def __init__( self, game_window : GameWindow ):
        self.game_window = game_window
        glClearColor( 255 / 255, 10 / 255, 10 / 255, 1.0 )  # red, green, blue, and alpha(transparency)

    def update( self, dt ):
        ...

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