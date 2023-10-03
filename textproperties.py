import customtkinter as ctk

INIT_TEXT = 'Sample'
INIT_SIZE = 35
INIT_OPACITY = 100
INIT_ROTATION = 0
INIT_COLOR = '#000000'
INIT_FONT = 'Courier'


class TextProperties:
    def __init__(self, pos_x, pos_y, update_func):
        self.text = ctk.StringVar(value=INIT_TEXT)
        self.size = ctk.IntVar(value=INIT_SIZE)
        self.rotation = ctk.DoubleVar(value=INIT_ROTATION)
        self.color = ctk.StringVar(value=INIT_COLOR)
        self.font = ctk.StringVar(value=INIT_FONT)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.canvas_id = None
        self.add_trace(update_func)

    def add_trace(self, update_func):
        self.text.trace_add(mode='write', callback=update_func)
        self.size.trace_add(mode='write', callback=update_func)
        self.rotation.trace_add(mode='write', callback=update_func)
        self.color.trace_add(mode='write', callback=update_func)
        self.font.trace_add(mode='write', callback=update_func)

    def copy(self, properties):
        self.text.set(properties.text.get())
        self.size.set(properties.size.get())
        self.color.set(properties.color.get())
        self.font.set(properties.font.get())
        self.rotation.set(properties.rotation.get())

    def update_text(self, text):
        self.text.set(text)

    def update_size(self, size):
        self.size.set(size)

    def update_rotation(self, rotation):
        self.rotation.set(rotation)

    def update_pos(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
