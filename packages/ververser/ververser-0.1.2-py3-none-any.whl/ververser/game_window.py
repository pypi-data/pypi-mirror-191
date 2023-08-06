import logging
from pathlib import Path
from time import time, sleep

import pyglet

from ververser.asset_manager import AssetManager, ReloadStatus
from ververser.fps_counter import FPSCounter
from ververser.script import load_script


logger = logging.getLogger(__name__)

EXPECTED_MAIN_SCRIPT_NAME = Path( 'main.py' )


class GameWindow( pyglet.window.Window ):

    def __init__( self, asset_folder_path : Path, throttle_fps = 30 ):
        super().__init__(vsync = False)

        self.throttle_fps = throttle_fps

        self.alive = True

        self.frame_count = 0
        self.last_update = time()
        self.fps_counter = FPSCounter()

        self.asset_manager = AssetManager( asset_folder_path )
        self.asset_manager.register_asset_loader( '.py', lambda p : load_script( p, self ) )
        self.main_script, load_status = self.asset_manager.load( EXPECTED_MAIN_SCRIPT_NAME )
        assert load_status == ReloadStatus.RELOADED, 'Could not load main script from example folder. Quitting.'

        self.is_initialised = False
        self.is_paused = False
        self.has_asset_problem = False

        self.init()

    def on_close(self):
        self.alive = False

    def run(self):
        while self.alive:
            self.dispatch_events()

            if self.is_paused:
                continue

            now = time()
            dt = now - self.last_update
            self.last_update = now

            if self.throttle_fps:
                sleep_time = ( 1 / self.throttle_fps ) - dt
                sleep( max( sleep_time, 0 ) )

            # TODO:
            # we do not want the framerate to affect physics
            # easiest way to do that is fix the dt here for now
            dt = 1/60

            reload_status = self.asset_manager.try_reload()
            if reload_status == ReloadStatus.FAILED:
                logger.info( "Error occured during asset loading. Game is now paused!" )
                self.has_asset_problem = True
                continue
            else:
                if reload_status == ReloadStatus.RELOADED:
                    self.has_asset_problem = False

            if self.is_paused or self.has_asset_problem:
                continue

            self._update(dt)
            self.update(dt)

            self._draw_start()
            self.draw()
            self._draw_end()

    def _update( self, dt ):
        self.fps_counter.update()

    def _draw_start( self ):
        self.clear()

    def _draw_end( self ):
        self.fps_counter.draw()
        self.flip()
        self.frame_count += 1

    # ---------------- Convenience Functions ----------------
    def try_invoke( self, f ):
        try :
            f()
        except :
            logging.exception( "Error occured during script invokation. Game is now paused!" )
            self.has_asset_problem = True

    # ================ End of standard boilerplate ================
    # ================ Overload the methods below! ================

    def init( self ):
        ...

    def update( self, dt ):
        self.try_invoke( lambda : self.main_script.get().update( dt ) )

    def draw( self ):
        self.try_invoke( lambda : self.main_script.get().draw() )