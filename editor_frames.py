import customtkinter as ctk
from panels import *
from textproperties import TextProperties


class EditorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky='nsew', pady=10, padx=10)


class TextEditorFrame(EditorFrame):
    def __init__(self, parent, text: TextProperties, delete_text, copy_text):
        super().__init__(parent)
        TextBoxPanel(self, text='Text', value=text.text)
        SlidePanel(self, text='Size', value=text.size, low_limit=0, high_limit=100)
        SlidePanel(self, text='Rotation', value=text.rotation, low_limit=-180, high_limit=180)
        ColorPanel(self, text.color)
        DoubleButtonPanel(self, "Remove", delete_text, "Copy", copy_text)


class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='green')
        self.pack(expand=True, fill='both')
