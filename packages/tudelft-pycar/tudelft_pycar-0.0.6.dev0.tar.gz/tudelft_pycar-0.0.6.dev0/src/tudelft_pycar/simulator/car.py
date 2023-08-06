import os
from traceback import format_exc
import pyglet
import numpy as np
from collections import deque
from ..path import relative_path
import math
from warnings import warn


class Car:
    # What is the height of the speaker? Assuming 20 cm for now
    speaker_height = 20

    def __init__(self, pycar_handle, start_position, batch):
        self.batch = batch
        self.pycar_handle = pycar_handle
        self.image = pyglet.image.load(os.path.join(relative_path, 'img', 'car.png'))
        self.image.anchor_x = self.image.width//2
        self.image.anchor_y = self.image.height//2
        self.sprite = pyglet.sprite.Sprite(self.image, start_position[0], start_position[1], batch=batch)
        self.serial_buffer = deque()

        self.reset(start_position)

    def reset(self, position):
        (x, y) = position
        self.speaker_position = np.array([x, y, self.speaker_height], dtype=float)
        self.angle = 0

        self.speed = 150
        self.attitude = 150

        self.audio_code = 0
        self.audio_enable = False
        self.bit_frequency = 5000
        self.carrier_frequency = 15000
        self.repetition_count = 2500  # The docs don't say what the default value is

        self.left_distance = 999
        self.right_distance = 999
        self.voltage = 18.0

    def draw(self):
        self.sprite.rotation = self.angle
        self.sprite.x = self.speaker_position[0]
        self.sprite.y = self.speaker_position[1]

    def act(self, delta_time):
        self.get_command()
        self.move(delta_time)
        self.draw()

    def get_command(self):
        self.serial_buffer.extend(self.pycar_handle._sim_serial_read_all())
        try:
            command_end = self.serial_buffer.index('\n'.encode('ASCII')[0])
        except ValueError:
            return

        command = []
        for i in range(command_end + 1):
            command.append(self.serial_buffer.popleft())

        try:
            self.handle_command(bytes(command))
        except ValueError as error:
            warn(format_exc())

    def handle_command(self, command):
        if b'\r' in command:
            raise ValueError("Windows style line ending (found '\\r' in command)")

        match command[0:1]:
            case b'M':
                value = int(command[1:4].decode('ASCII'))
                if not 135 <= value <= 165:
                    raise ValueError("Value out of bounds: " + str(value))
                self.speed = value

            case b'D':
                value = int(command[1:4].decode('ASCII'))
                if not 100 <= value <= 200:
                    raise ValueError("Value out of bounds: " + str(value))
                self.attitude = value

            case b'A':
                if command[1:2] == b'1':
                    self.audio_enable = True
                else:
                    self.audio_enable = False

            case b'B':
                self.bit_frequency = int.from_bytes(command[1:3], byteorder='big')

            case b'F':
                self.carrier_frequency = int.from_bytes(command[1:3], byteorder='big')

            case b'C':
                self.audio_code = int.from_bytes(command[1:5], byteorder='big')

            case b'R':
                value = int.from_bytes(command[1:3], byteorder='big')
                if value < 32:
                    raise ValueError("Repetition count cannot be less than 32")

                self.repetition_count = value

            case b'S':
                match command[1:2]:
                    case b'd':
                        status = "USL{}\nUSR{}\n\x04".format(self.left_distance, self.right_distance)
                    case b'v':
                        status = """VBATT{:.2f}V\n\x04""".format(self.voltage)
                    case _:
                        status = '**************************\n'
                        status += '* Audio Beacon: {}\n'.format('on' if self.audio_enable else 'off')
                        status += '* c: {:#x}\n'.format(self.audio_code)
                        status += '* f_c: {}\n'.format(self.carrier_frequency)
                        status += '* f_b: {}\n'.format(self.bit_frequency)
                        status += '* c_r: {}\n'.format(self.repetition_count)
                        status += '**************************\n'
                        status += '* PWM:\n'
                        status += '* Dir. {}\n'.format(self.attitude)
                        status += '* Mot. {}\n'.format(self.speed)
                        status += '**************************\n'
                        status += '* Sensors:\n'
                        status += '* Dist. L {} R {}\n'.format(self.left_distance, self.right_distance)
                        status += '* V_batt {} V\n'.format(self.voltage)
                        status += '**************************\n\x04'

                self.pycar_handle._sim_serial_write(status.encode('ASCII'))

            case b'V':
                # No, I'm not keeping this up to date
                version = '*******************************\n' \
                          '*            EPO-4            *\n' \
                          '*******************************\n' \
                          '* Virtual KITT   Rev.  1.0    *\n' \
                          '* Audio Firmware Rev.  0.0    *\n' \
                          '*******************************\n' \
                          '*   Author:  A. Stijns  B.Sc. *\n' \
                          '*   Date:     Feb 6, 2023     *\n' \
                          '*******************************\n\x04'

                self.pycar_handle._sim_serial_write(version.encode('ASCII'))

            case _:
                raise ValueError("Unknown command: " + str(bytes([command[0]])))

    def move(self, delta_time):
        real_attitude = -(self.attitude-150)/50.
        real_speed = -(self.speed-150)/7.5*delta_time*60
        self.angle += real_attitude * real_speed

        direction_y = -math.cos(math.radians(self.angle))
        direction_x = -math.sin(math.radians(self.angle))

        velocity = np.array([direction_x, direction_y, 0]) * real_speed
        self.speaker_position += velocity
