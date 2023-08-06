from pathlib import Path
from typing import Any

from runpy import run_path


def invoke_if_available( f, *args, **kwargs ):
    if f:
        f(*args, **kwargs)


class Script:

    def __init__( self, file_path : Path, game ):
        self.file_path = file_path
        data_module = run_path( str( file_path ) )

        self.f_init = data_module.get( 'init' )
        self.f_update = data_module.get( 'update' )
        self.f_draw = data_module.get( 'draw' )

        self.init( game )

    def init( self, game_window ):
        invoke_if_available( self.f_init, game_window )

    def update( self, dt ) -> None:
        invoke_if_available( self.f_update, dt )

    def draw( self ) -> None:
        invoke_if_available( self.f_draw )


def load_script( script_path : Path, game ) -> Any:
    return Script( script_path, game )
