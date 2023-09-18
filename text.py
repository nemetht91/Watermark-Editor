import customtkinter as ctk

INIT_TEXT = 'Sample'
INIT_SIZE = 20
INIT_OPACITY = 100
INIT_ROTATION = 0
INIT_POS_X = 0
INIT_POS_Y = 0


class Text:
    def __init__(self):
        self.text = ctk.StringVar(value=INIT_TEXT)
        self.size = ctk.DoubleVar(value=INIT_SIZE)
        self.opacity = ctk.DoubleVar(value=INIT_OPACITY)
        self.rotation = ctk.DoubleVar(value=INIT_ROTATION)
        self.pos_x = INIT_POS_X
        self.pos_y = INIT_POS_Y

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
