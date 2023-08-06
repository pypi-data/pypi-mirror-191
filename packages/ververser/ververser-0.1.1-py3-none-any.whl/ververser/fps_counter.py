from time import time

import pyglet


class FPSCounter:

    def __init__(self):
        self.frames = 0
        self.total_frames = 0
        self.framerate = pyglet.text.Label(
            text='Unknown',
            font_name='Verdana',
            font_size=8,
            x=10,
            y=10,
            color=(255,255,255,255)
        )
        self.last_frame = time()
        self.fps = 0

    def update( self ):
        last_frame_dt = time() - self.last_frame
        self.frames += 1
        self.total_frames += 1
        if last_frame_dt >= 1 :
            self.fps = self.frames
            self.framerate.text = str( self.fps )
            self.frames = 0
            self.last_frame = time()

    def draw( self ):
        self.framerate.draw()
