import sys
from warnings import warn
import traceback
import argparse
import serial
from serial.tools.list_ports import comports
import pygame
import pygame_gui
import numpy as np
import pyaudio

parser = argparse.ArgumentParser(prog='Virtual KITT', epilog='')
parser.add_argument('-p', '--port', default=comports()[0].device, help="""
    Virtual serial port to attach to
    (tip: use com0com <https://com0com.sourceforge.net> to create virtual ports on Windows)
""")
parser.add_argument('--list-ports',
                    help="List available serial ports",
                    action='store_true')
args = parser.parse_args(sys.argv[1:])

if args.list_ports:
    if not comports():
        print("No serial ports found")
    else:
        print("Serial ports:")
        for port in comports():
            print(port)

    exit()

com_port = args.port
print("Using serial port:", com_port)
serial_port = serial.Serial(com_port, 115200, rtscts=True)

SCREEN_SIZE = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()

pygame.display.set_caption("KITT Demo App")
pygame.display.set_icon(pygame.image.load('img/window-icon.png'))

screen.fill(0x101020)
pygame.display.flip()

pygame.font.init()
font = pygame.font.SysFont('monospace', 20)


def text(string, position, color):
    screen.blit(font.render(string, False, color), position)


text('W', (240, 5), 0x88888800)
text('S', (240, 25), 0x88888800)
text('A', (220, 25), 0x88888800)
text('D', (260, 25), 0x88888800)

manager = pygame_gui.UIManager((SCREEN_SIZE, SCREEN_SIZE))


def make_box(index, text, default=""):
    text_rect = pygame.Rect((0, index*40), (100, 40))
    box_rect = pygame.Rect((100, index*40), (100, 40))
    text = pygame_gui.elements.UITextBox(text, text_rect, manager)
    box = pygame_gui.elements.UITextEntryLine(box_rect, manager, initial_text=default)
    return text, box


def make_buttons(index):
    start = pygame_gui.elements.UIButton(pygame.Rect((0, index*40), (100, 40)), "Start", manager)
    stop = pygame_gui.elements.UIButton(pygame.Rect((100, index*40), (100, 40)), "Stop", manager)
    return start, stop


(_, code_box) = make_box(0, "Code:", "00000000")
(_, carrier_box) = make_box(1, "Carrier:", "15000")
(_, bit_box) = make_box(2, "Bit Freq.:", "5000")
(_, repeat_box) = make_box(3, "Repeat:", "2500")
(start_button, stop_button) = make_buttons(4)

status_button = pygame_gui.elements.UIButton(pygame.Rect((200, 80), (100, 40)), "Status", manager)
status_text = pygame_gui.elements.UITextBox("", pygame.Rect((0, 205), (240, 395)), manager)


def list_input_devices(pyaudio_handle):
    device_list = []

    for i in range(pyaudio_handle.get_device_count()):
        device_info = pyaudio_handle.get_device_info_by_index(i)
        if device_info['maxInputChannels'] >= 5:
            device_list.append(i)

    return device_list


pyaudio_handle = pyaudio.PyAudio()
audio_device_index = 2#list_input_devices(pyaudio_handle)[-1]
audio_device_name = pyaudio_handle.get_device_info_by_index(audio_device_index)['name']
print("Audio devices:")
for device in list_input_devices(pyaudio_handle):
    device_name = pyaudio_handle.get_device_info_by_index(device)['name']
    max_input_channels = pyaudio_handle.get_device_info_by_index(device)['maxInputChannels']
    host_api = pyaudio_handle.get_device_info_by_index(device)['hostApi']
    host_api_name = pyaudio_handle.get_host_api_info_by_index(host_api)['name']
    print("Index: {:2d}  Name: {}  Channels: {}  Host API: {}"
          .format(device, device_name, max_input_channels, host_api_name))

print("Using audio device: {} [{}]".format(audio_device_index, audio_device_name))
print(pyaudio_handle.get_device_info_by_index(audio_device_index))
print(pyaudio_handle.get_host_api_info_by_index(3))


SAMPLE_FREQ = 96000
SAMPLE_FMT = pyaudio.paInt16
CHANNELS = 5

stream = pyaudio_handle.open(input_device_index=audio_device_index,
                             channels=CHANNELS,
                             format=SAMPLE_FMT,
                             rate=SAMPLE_FREQ,
                             input=True)


def plot_audio(screen):
    pygame.draw.rect(screen, 0, pygame.Rect(SCREEN_SIZE-200, 0, 200, SCREEN_SIZE))
    data = np.frombuffer(stream.read(int(SAMPLE_FREQ*CHANNELS/60)), dtype='uint16')
    deinterlaced = [data[i::CHANNELS] for i in range(CHANNELS)]
    for i in range(CHANNELS):
        power = np.sqrt(np.mean(np.square(deinterlaced[i])))
        power *= (SCREEN_SIZE/CHANNELS)/200
        pos = (i+1)*SCREEN_SIZE/CHANNELS
        pygame.draw.line(screen, 0xFFFFFF, (SCREEN_SIZE-10, pos-power), (SCREEN_SIZE, pos-power))

        pygame.draw.line(screen, 0x888888, (SCREEN_SIZE-200, pos), (SCREEN_SIZE, pos))


window_closed = False
while not window_closed:
    time_delta = clock.tick(60) / 1000.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_closed = True
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w:
                    serial_port.write(b'M165\n')
                    text('W', (240, 5), 0x00FF0000)
                case pygame.K_s:
                    serial_port.write(b'M135\n')
                    text('S', (240, 25), 0x00FF0000)
                case pygame.K_a:
                    serial_port.write(b'D100\n')
                    text('A', (220, 25), 0x00FF0000)
                case pygame.K_d:
                    serial_port.write(b'D200\n')
                    text('D', (260, 25), 0x00FF0000)
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                serial_port.write(b'M150\n')
                text('W', (240, 5), 0x88888800)
                text('S', (240, 25), 0x88888800)
            if event.key in (pygame.K_a, pygame.K_d):
                serial_port.write(b'D150\n')
                text('A', (220, 25), 0x88888800)
                text('D', (260, 25), 0x88888800)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                try:
                    code = int(code_box.text, 16).to_bytes(4, byteorder='big')
                    carrier_frequency = int(carrier_box.text, 10).to_bytes(2, byteorder='big')
                    bit_frequency = int(bit_box.text, 10).to_bytes(2, byteorder='big')
                    repeat_count = int(repeat_box.text, 10).to_bytes(2, byteorder='big')
                except (OverflowError, ValueError):
                    warn(traceback.format_exc())
                else:
                    serial_port.write(b'C'+code+b'\n')
                    serial_port.write(b'F'+carrier_frequency+b'\n')
                    serial_port.write(b'B'+bit_frequency+b'\n')
                    serial_port.write(b'R'+repeat_count+b'\n')
                    serial_port.write(b'A1\n')
            if event.ui_element == stop_button:
                serial_port.write(b'A0\n')

            if event.ui_element == status_button:
                serial_port.write(b'S\n')
                status = serial_port.read_until(b'\x04')
                status_text.set_text(status[:-2].decode('ASCII'))

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(screen)

    plot_audio(screen)

    pygame.display.flip()

pygame.quit()
