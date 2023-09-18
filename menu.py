import customtkinter as ctk
from panels import *


class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky='nsew', pady=10, padx=10)
        self.add('Add Text')
        self.add('Color')
        self.add('Effects')
        self.add('Export')

        TextEditorFrame(self.tab('Add Text'))
        ColorFrame(self.tab('Color'))


class TextEditorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.size = ctk.DoubleVar(value=0)
        self.opacity = ctk.DoubleVar(value=0)
        self.rotation = ctk.DoubleVar(value=0)
        TextBoxPanel(self, text='Text')
        SlidePanel(self, text='Size', value=self.size, low_limit=0, high_limit=100)
        SlidePanel(self, text='Opacity', value=self.opacity, low_limit=0, high_limit=100)
        SlidePanel(self, text='Rotation', value=self.rotation, low_limit=-180, high_limit=180)


class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='green')
        self.pack(expand=True, fill='both')
