import serial
import numpy as np
from .settings import settings
from collections import deque


class PyCar:
    def __init__(self, simulated=True):
        self.simulated = simulated

        if self.simulated:
            self.tx_dequeue = deque()
            self.rx_dequeue = deque()
            self.audio_dequeue = deque()

        if settings.com_port:
            self.serial = serial.Serial(settings.com_port, 115200, rtscts=True)
        if settings.audio_device_index:
            self.stream = settings.pyaudio_handle.open(output_device_index=settings.audio_device_index,
                                                       channels=5,
                                                       format=settings.SAMPLE_FMT,
                                                       rate=settings.SAMPLE_FREQ,
                                                       output=True)

    def serial_write(self, data: bytes):
        if self.simulated:
            self.tx_dequeue.extend(data)
        else:
            self.serial.write(data)

    def serial_read(self):
        if self.simulated:
            try:
                response = self.rx_dequeue.popleft()
            except IndexError:
                response = b''

            return response
        else:
            return self.serial.read_until(b'\x04')

    def audio_read(self, num_frames):
        if self.simulated:
            return np.zeros(num_frames*settings.CHANNELS)
        else:
            return np.frombuffer(self.stream.read(num_frames), dtype='uint16')

    def _sim_serial_read_all(self):
        result = []
        for char in self.tx_dequeue:
            result.append(char)
        self.tx_dequeue.clear()

        return bytes(result)

    def _sim_serial_write(self, data: bytes):
        # note: this is appending a set of bytes, *not* extending the dequeue with chars!
        self.rx_dequeue.append(data)

    def _sim_audio_write(self, frames: bytes):
        self.audio_dequeue.extend(frames)
