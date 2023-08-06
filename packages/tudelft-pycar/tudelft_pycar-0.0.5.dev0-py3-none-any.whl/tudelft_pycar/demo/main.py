import os
from warnings import warn
import traceback
import pyglet
import numpy as np
import pyaudio
from ..path import relative_path

SCREEN_SIZE = 600

background_color = (16, 16, 32, 255)
background_color_gl = [c/255. for c in background_color]
highlight_color = [c+10 for c in background_color[0:3]]
passive_color = (180, 180, 180, 255)
active_color = (130, 255, 130, 255)

color_w = passive_color
color_s = passive_color
color_a = passive_color
color_d = passive_color


class Button(object):
    def __init__(self, text, x, y, on_click, batch):
        self.on_click = on_click
        pad = 5
        self.width = 70
        self.height = 30
        self.rect = pyglet.shapes.Rectangle(x, y, self.width, self.height, color=highlight_color, batch=batch)
        self.label = pyglet.text.Label(text, x=x+self.width/2, y=y+pad,
                                       anchor_x='center', color=passive_color, batch=batch)

    def hit_test(self, x, y):
        if 0 < x - self.rect.x < self.rect.width and 0 < y - self.rect.y < self.rect.height:
            self.on_click()
            self.label.color = active_color

    def release_test(self, x, y):
        if 0 < x - self.rect.x < self.rect.width and 0 < y - self.rect.y < self.rect.height:
            self.label.color = passive_color


class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
                                dict(color=passive_color)
                                )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)
        self.caret.color = passive_color[0:3]
        self.caret.visible = False

        self.layout.x = x
        self.layout.y = y

        '''
        pad = 2
        self.rectangle = pyglet.shapes.Rectangle(x - pad, y - pad,
                                                 x + width + pad, y + height + pad,
                                                 color=background_color, batch=batch)
        '''

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)


def make_input(string, default, index, batch):
    y_position = index*40+20
    label = pyglet.text.Label(string, x=10, y=y_position, anchor_y='bottom',
                             color=passive_color, batch=batch)
    widget = TextWidget(default, 80, y_position, 100, batch)
    return label, widget


class Window(pyglet.window.Window):
    def __init__(self, pycar_handle, *args, **kwargs):
        super(Window, self).__init__(SCREEN_SIZE, SCREEN_SIZE, caption='KITT Demo')
        self.pycar = pycar_handle

        self.batch = pyglet.graphics.Batch()
        self.labels = [
            make_input('Code', '00000000', 3, self.batch),
            make_input('Carrier', '15000', 2, self.batch),
            make_input('Bit Freq.', '5000', 1, self.batch),
            make_input('Repeat', '2500', 0, self.batch),
        ]
        self.widgets = [w[1] for w in self.labels]
        self.text_cursor = self.get_system_mouse_cursor('text')

        self.focus = None
        self.set_focus(self.widgets[0])

        self.buttons = [
            Button('Start', 200, 5, self.start_audio, self.batch),
            Button('Stop', 200, 45, self.stop_audio, self.batch),
            Button('Status', 200, 85, self.get_status, self.batch)
        ]

        self.wasd = [
            pyglet.text.Label('W', x=240, y=140, anchor_x='center', color=passive_color, batch=self.batch),
            pyglet.text.Label('A', x=220, y=120, anchor_x='center', color=passive_color, batch=self.batch),
            pyglet.text.Label('S', x=240, y=120, anchor_x='center', color=passive_color, batch=self.batch),
            pyglet.text.Label('D', x=260, y=120, anchor_x='center', color=passive_color, batch=self.batch)
        ]

        self.status_document = pyglet.text.document.UnformattedDocument('No\nstatus')
        self.status_document.set_style(0, len(self.status_document.text),
                                dict(color=passive_color)
                                )
        self.status_text = pyglet.text.layout.TextLayout(self.status_document, multiline=True,
                                                         width=200, height=300, batch=self.batch)
        self.status_text.x = 5
        self.status_text.y = SCREEN_SIZE-self.status_text.height

    def start_audio(self):
        code, carrier, bit_frequency, repeat_count = [widget.document.text for widget in self.widgets]
        try:
            code = int(code, 16).to_bytes(4, byteorder='big')
            carrier_frequency = int(carrier, 10).to_bytes(2, byteorder='big')
            bit_frequency = int(bit_frequency, 10).to_bytes(2, byteorder='big')
            repeat_count = int(repeat_count, 10).to_bytes(2, byteorder='big')
        except (OverflowError, ValueError):
            warn(traceback.format_exc())
        else:
            self.pycar.serial_write(b'C'+code+b'\n')
            self.pycar.serial_write(b'F'+carrier_frequency+b'\n')
            self.pycar.serial_write(b'B'+bit_frequency+b'\n')
            self.pycar.serial_write(b'R'+repeat_count+b'\n')
            self.pycar.serial_write(b'A1\n')

    def stop_audio(self):
        self.pycar.serial_write(b'A0\n')

    def get_status(self):
        self.pycar.serial_write(b'S\n')
        status = self.pycar.serial_read()

        self.status_document.text = status.decode('ASCII')

    def on_draw(self):
        pyglet.gl.glClearColor(background_color_gl[0],
                               background_color_gl[1],
                               background_color_gl[2],
                               background_color_gl[3])
        self.clear()
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)

        for button in self.buttons:
            button.hit_test(x, y)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for button in self.buttons:
            button.release_test(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                dir = -1
            else:
                dir = 1

            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                dir = 0

            self.set_focus(self.widgets[(i + dir) % len(self.widgets)])

        elif symbol == pyglet.window.key.W:
            self.wasd[0].color = active_color
            self.pycar.serial_write(b'M165\n')
        elif symbol == pyglet.window.key.A:
            self.wasd[1].color = active_color
            self.pycar.serial_write(b'D100\n')
        elif symbol == pyglet.window.key.S:
            self.wasd[2].color = active_color
            self.pycar.serial_write(b'M135\n')
        elif symbol == pyglet.window.key.D:
            self.wasd[3].color = active_color
            self.pycar.serial_write(b'D200\n')

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def on_key_release(self, symbol, modifiers):
        if symbol in (pyglet.window.key.W, pyglet.window.key.S):
            self.wasd[0].color = passive_color
            self.wasd[2].color = passive_color
            self.pycar.serial_write(b'M150\n')
        elif symbol in (pyglet.window.key.A, pyglet.window.key.D):
            self.wasd[1].color = passive_color
            self.wasd[3].color = passive_color
            self.pycar.serial_write(b'D150\n')

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)


def run(pycar_handle):
    window1 = pyglet.window.Window(width=SCREEN_SIZE, height=SCREEN_SIZE)
    window1.set_caption("KITT Demo")
    window1.set_icon(pyglet.image.load(os.path.join(relative_path, 'img', 'window-icon.png')))

    def text(string, position, color, batch):
        return pyglet.text.Label(string,
                                 font_name='monospace',
                                 font_size=20, color=color,
                                 x=position[0], y=position[1], batch=batch)


    def make_box(index, string, default="", batch=None):
        #text_rect = pygame.Rect((0, index*40), (100, 40))
        #box_rect = pygame.Rect((100, index*40), (100, 40))
        label = text(string, (5, SCREEN_SIZE-(index+1)*40+5), passive_color, batch=batch)
        #box = pyglet.gui.TextEntry(default, 205, SCREEN_SIZE-(index+1)*40+5, 100, batch=batch)

        document = pyglet.text.document.UnformattedDocument(string)
        box = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)
        #box = pygame_gui.elements.UITextEntryLine(box_rect, manager, initial_text=default)
        return label, box

    @window1.event
    def on_key_press(symbol, modifiers):
        global color_a, color_d, color_w, color_s
        match symbol:
            case pyglet.window.key.W:
                color_w = active_color
                pycar_handle.serial_write(b'M165\n')
            case pyglet.window.key.S:
                color_s = active_color
                pycar_handle.serial_write(b'M135\n')
            case pyglet.window.key.A:
                color_a = active_color
                pycar_handle.serial_write(b'D100\n')
            case pyglet.window.key.D:
                color_d = active_color
                pycar_handle.serial_write(b'D200\n')


    @window1.event
    def on_key_release(symbol, modifiers):
        global color_a, color_d, color_w, color_s
        if symbol in (pyglet.window.key.W, pyglet.window.key.S):
            color_w = color_s = passive_color
            pycar_handle.serial_write(b'M150\n')
        if symbol in (pyglet.window.key.A, pyglet.window.key.D):
            color_a = color_d = passive_color
            pycar_handle.serial_write(b'D150\n')

    @window1.event
    def on_draw():
        batch = pyglet.graphics.Batch()
        rectangle = pyglet.shapes.Rectangle(0, 0, SCREEN_SIZE, SCREEN_SIZE,
                                            color=(16, 16, 32), batch=batch)

        label_w = text('W', (340, SCREEN_SIZE-30), color_w, batch)
        label_s = text('S', (340, SCREEN_SIZE-60), color_s, batch)
        label_a = text('A', (310, SCREEN_SIZE-60), color_a, batch)
        label_d = text('D', (370, SCREEN_SIZE-60), color_d, batch)

        (code_label, code_box) = make_box(0, "Code:", "00000000", batch=batch)
        (carrier_label, carrier_box) = make_box(1, "Carrier:", "15000", batch=batch)
        (bit_label, bit_box) = make_box(2, "Bit Freq.:", "5000", batch=batch)
        (repeat_label, repeat_box) = make_box(3, "Repeat:", "2500", batch=batch)

        batch.draw()

    return


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
