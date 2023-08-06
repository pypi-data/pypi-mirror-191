import pygame
import pyaudio
import numpy as np
from src.tudelft_pycar.settings import settings
from car import car


def audio_callback(in_data, frame_count, time_info, status):
    data_len = frame_count*5
    # should be just junk
    if car.audio_enable:
        data = np.linspace(0.0, 1.0, data_len)
    else:
        data = np.zeros(data_len)
    return data, pyaudio.paContinue


class Microphones:
    def __init__(self, pyaudio_handle):
        self.image = pygame.image.load('img/microphone.png')
        self.pyaudio = pyaudio_handle
        self.stream = self.pyaudio.open(output_device_index=settings.audio_device_index,
                                        stream_callback=audio_callback,
                                        channels=5,
                                        format=settings.SAMPLE_FMT,
                                        rate=settings.SAMPLE_FREQ,
                                        output=True)

        self.positions = self.generate_positions()

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
        base_height = 30
        mic5_height = 50
        positions = [pygame.math.Vector3(0, 0, base_height)]
        positions += [pygame.math.Vector3(settings.SQUARE_SIZE, 0, base_height)]
        positions += [pygame.math.Vector3(settings.SQUARE_SIZE, settings.SQUARE_SIZE, base_height)]
        positions += [pygame.math.Vector3(0, settings.SQUARE_SIZE, base_height)]
        positions += [pygame.math.Vector3(0, settings.SQUARE_SIZE / 2, mic5_height)]

        margin = (settings.SCREEN_SIZE - settings.SQUARE_SIZE) / 2
        offset = pygame.math.Vector3(margin, margin, 0)
        for position in positions:
            position += offset

        return positions

    def draw(self, surface):
        draw_lines(surface)

        for position in self.positions:
            (x, y) = (position[0], position[1])
            rect = self.image.get_rect(center=(x, y))
            surface.blit(self.image, rect)

    def act(self):
        if not self.stream.is_active():
            raise ValueError('Audio stream was deactivated')


def draw_lines(surface):
    margin = (settings.SCREEN_SIZE - settings.SQUARE_SIZE) / 2
    rect = pygame.Rect(margin, margin, settings.SQUARE_SIZE, settings.SQUARE_SIZE)
    pygame.draw.rect(surface, 0x808080, rect, 2)
    for x in range(0, settings.SQUARE_SIZE, 50):
        pygame.draw.line(surface, 0xAAAAAA,
                         (x + margin, margin),
                         (x + margin, settings.SQUARE_SIZE + margin - 2))
    for y in range(0, settings.SQUARE_SIZE, 50):
        pygame.draw.line(surface, 0xAAAAAA,
                         (margin, y + margin),
                         (margin + settings.SQUARE_SIZE - 2, y + margin))
