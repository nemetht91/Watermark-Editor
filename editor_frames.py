import customtkinter as ctk
from panels import *
from textproperties import TextProperties


class EditorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky='nsew', pady=10, padx=10)


class TextEditorFrame(EditorFrame):
    def __init__(self, parent, text: TextProperties):
        super().__init__(parent)
        self.size = text.size
        self.opacity = text.opacity
        self.rotation = text.rotation
        TextBoxPanel(self, text='Text', value=text.text)
        SlidePanel(self, text='Size', value=self.size, low_limit=0, high_limit=100)
        SlidePanel(self, text='Opacity', value=self.opacity, low_limit=0, high_limit=100)
        SlidePanel(self, text='Rotation', value=self.rotation, low_limit=-180, high_limit=180)


class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='green')
        self.pack(expand=True, fill='both')
