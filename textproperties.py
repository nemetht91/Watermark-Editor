import customtkinter as ctk

INIT_TEXT = 'Sample'
INIT_SIZE = 20
INIT_OPACITY = 100
INIT_ROTATION = 0


class TextProperties:
    def __init__(self, pos_x, pos_y):
        self.text = ctk.StringVar(value=INIT_TEXT)
        self.size = ctk.DoubleVar(value=INIT_SIZE)
        self.opacity = ctk.DoubleVar(value=INIT_OPACITY)
        self.rotation = ctk.DoubleVar(value=INIT_ROTATION)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.canvas_id = None
        self.callback_name = None

    def add_text_trace(self, update_func):
        self.callback_name = self.text.trace_add(mode='write', callback=update_func)

    def remove_text_trace(self):
        self.text.trace_remove(mode='write', cbname=self.callback_name)

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
