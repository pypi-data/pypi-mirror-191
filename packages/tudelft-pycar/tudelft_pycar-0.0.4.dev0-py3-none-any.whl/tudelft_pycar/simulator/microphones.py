import pyglet
import os
import pyaudio
import numpy as np
from ..settings import settings
from ..path import relative_path


def audio_callback(in_data, frame_count, time_info, status):
    data_len = frame_count * 2
    # should be just junk
    data = np.linspace(0.0, 1.0, data_len)
    return data, pyaudio.paContinue


class Microphones:
    def __init__(self, pycar_handle, pyaudio_handle, batch):
        self.batch = batch
        self.pycar_handle = pycar_handle
        self.image = pyglet.image.load(os.path.join(relative_path, 'img', 'microphone.png'))
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
        self.pyaudio = pyaudio_handle

        self.positions = self.generate_positions()
        self.draw()

    @staticmethod
    def generate_positions():
        """
        Microphone positions:
        4---3
        |   |
        5   |
        |   |
        1---2
        Square is 600x600 cm
        Microphones 1-4 are 30 cm up
        Microphone 5 is 50 cm up
        """
        base_height = 30.
        mic5_height = 50.
        positions = [np.array([0., 0, base_height])]
        positions += [np.array([settings.SQUARE_SIZE, 0., base_height])]
        positions += [np.array([settings.SQUARE_SIZE, settings.SQUARE_SIZE, base_height])]
        positions += [np.array([0., settings.SQUARE_SIZE, base_height])]
        positions += [np.array([0., settings.SQUARE_SIZE / 2, mic5_height])]

        margin = (settings.SCREEN_SIZE - settings.SQUARE_SIZE) / 2
        offset = np.array([margin, margin, 0.])
        for position in positions:
            position += offset

        return positions

    def draw(self):
        self.lines = draw_lines(self.batch)

        self.sprites = []
        for position in self.positions:
            (x, y) = (position[0], position[1])
            self.sprites.append(pyglet.sprite.Sprite(self.image, x, y, batch=self.batch))

    def act(self, delta_time):
        frames = int(settings.SAMPLE_FREQ * delta_time * settings.CHANNELS)
        data = audio_callback(None, frames, None, None)
        self.pycar_handle._sim_audio_write(data)


def draw_lines(batch):
    lines = []
    margin = (settings.SCREEN_SIZE - settings.SQUARE_SIZE) / 2
    for x in range(0, settings.SQUARE_SIZE + 1, 50):
        lines.append(pyglet.shapes.Line(x + margin, margin,
                                        x + margin, settings.SQUARE_SIZE + margin,
                                        color=(170, 170, 170), batch=batch))
    for y in range(0, settings.SQUARE_SIZE + 1, 50):
        lines.append(pyglet.shapes.Line(margin, y + margin,
                                        margin + settings.SQUARE_SIZE, y + margin,
                                        color=(170, 170, 170), batch=batch))

    return lines
