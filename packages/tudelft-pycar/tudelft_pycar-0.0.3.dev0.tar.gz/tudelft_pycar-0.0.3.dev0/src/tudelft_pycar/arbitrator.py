import serial
import numpy as np
from settings import settings


class PyCar:
    def __init__(self, simulated=False):
        self.simulated = simulated
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
            return
        else:
            self.serial.write(data)

    def serial_read(self):
        if self.simulated:
            return b''
        else:
            return self.serial.read_until(b'\x04')

    def audio_read(self, num_frames):
        if self.simulated:
            return np.zeros(num_frames*settings.CHANNELS)
        else:
            return np.frombuffer(self.stream.read(num_frames), dtype='uint16')
