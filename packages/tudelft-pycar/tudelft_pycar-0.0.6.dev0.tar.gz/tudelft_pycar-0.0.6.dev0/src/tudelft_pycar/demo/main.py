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
