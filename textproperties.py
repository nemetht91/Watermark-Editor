import customtkinter as ctk

INIT_TEXT = 'Sample'
INIT_SIZE = 35
INIT_OPACITY = 100
INIT_ROTATION = 0
INIT_COLOR = 'red'
INIT_FONT = 'Courier'


class TextProperties:
    def __init__(self, pos_x, pos_y, update_func):
        self.text = ctk.StringVar(value=INIT_TEXT)
        self.size = ctk.IntVar(value=INIT_SIZE)
        self.opacity = ctk.DoubleVar(value=INIT_OPACITY)
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
        self.opacity.trace_add(mode='write', callback=update_func)
        self.rotation.trace_add(mode='write', callback=update_func)

    def update_text(self, text):
        self.text.set(text)

    def update_size(self, size):
        self.size.set(size)

    def update_opacity(self, opacity):
        self.opacity.set(opacity)

    def update_rotation(self, rotation):
        self.rotation.set(rotation)

    def update_pos(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
