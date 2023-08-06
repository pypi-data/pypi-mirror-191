import sys
import argparse
from serial.tools.list_ports import comports
import pyaudio


def list_output_devices(pyaudio_handle):
    device_list = []

    for i in range(pyaudio_handle.get_device_count()):
        device_info = pyaudio_handle.get_device_info_by_index(i)
        if device_info['maxOutputChannels'] >= 5:
            device_list.append(i)

    return device_list


class Settings:
    def __init__(self):
        self.SQUARE_SIZE = 600
        self.SCREEN_SIZE = self.SQUARE_SIZE + 100
        self.SAMPLE_FREQ = 96000
        self.SAMPLE_FMT = pyaudio.paInt16
        self.CHANNELS = 5

        self.pyaudio_handle = pyaudio.PyAudio()

        try:
            default_serial = comports()[0].device
        except IndexError:
            default_serial = None

        parser = argparse.ArgumentParser(prog='Virtual KITT', epilog='')
        parser.add_argument('-p', '--port', default=default_serial, help="""
            Virtual serial port to attach to
            (tip: use com0com <https://com0com.sourceforge.net> to create virtual ports on Windows)
        """)

        try:
            default_audio = list_output_devices(self.pyaudio_handle)[-1]
        except IndexError:
            default_audio = None

        parser.add_argument('-a', '--audio',
                            type=int,
                            default=default_audio,
                            help="""
            Audio device index to use
            (tip: use VB-Cable <https://vb-audio.com/Cable/> to create a virtual audio device)
        """)
        parser.add_argument('--list-audio-devices',
                            help="List available audio devices",
                            action='store_true')
        parser.add_argument('--list-ports',
                            help="List available serial ports",
                            action='store_true')
        args = parser.parse_args(sys.argv[1:])
        if args.list_audio_devices:
            if not list_output_devices(self.pyaudio_handle):
                print("No suitable output devices (is VB-Cable <https://vb-audio.com/Cable/> installed?)")
            else:
                print("Audio devices:")
                for device in list_output_devices(self.pyaudio_handle):
                    device_name = self.pyaudio_handle.get_device_info_by_index(device)['name']
                    max_output_channels = self.pyaudio_handle.get_device_info_by_index(device)['maxOutputChannels']
                    host_api = self.pyaudio_handle.get_device_info_by_index(device)['hostApi']
                    host_api_name = self.pyaudio_handle.get_host_api_info_by_index(host_api)['name']
                    print("Index: {:2d}  Name: {}  Channels: {}  Host API: {}"
                          .format(device, device_name, max_output_channels, host_api_name))

        if args.list_ports:
            if not comports():
                print("No serial ports found")
            else:
                print("Serial ports:")
                for port in comports():
                    print(port)

        if args.list_audio_devices or args.list_ports:
            exit()

        self.com_port = args.port
        self.audio_device_index = args.audio
        print("Using serial port:", self.com_port)
        audio_device_name = self.pyaudio_handle.get_device_info_by_index(self.audio_device_index)['name']
        print("Using audio device: {} [{}]".format(self.audio_device_index, audio_device_name))


settings = Settings()
