import pyglet
import os
from .car import Car
from ..path import relative_path
from .microphones import Microphones
from ..settings import settings


class Window(pyglet.window.Window):
    def __init__(self, pycar_handle, *args, **kwargs):
        super(Window, self).__init__(settings.SCREEN_SIZE, settings.SCREEN_SIZE, caption='Virtual KITT')

        self.batch = pyglet.graphics.Batch()

        self.microphones = Microphones(pycar_handle, settings.pyaudio_handle, self.batch)

        margin = (settings.SCREEN_SIZE - settings.SQUARE_SIZE) / 2
        self.car = Car(pycar_handle, (settings.SCREEN_SIZE / 2, margin), self.batch)

        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def update(self, delta_time):
        self.microphones.act(delta_time)
        self.car.act(delta_time)

    def on_draw(self):
        pyglet.gl.glClearColor(0.20, 0.19, 0.25, 1)
        self.clear()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.car.reset((x, y))
