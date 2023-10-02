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
        self.color = text.color
        TextBoxPanel(self, text='Text', value=text.text)
        SlidePanel(self, text='Size', value=self.size, low_limit=0, high_limit=100)
        SlidePanel(self, text='Opacity', value=self.opacity, low_limit=0, high_limit=100)
        SlidePanel(self, text='Rotation', value=self.rotation, low_limit=-180, high_limit=180)
        ColorEditor(self, self.color)


class ColorEditor:
    def __init__(self, parent, value):
        #ctk.CTkLabel(parent, text="Color").grid(column=0, row=0, sticky='W', padx=5)
        self.color = value
        self.red = ctk.IntVar(value=0)
        self.green = ctk.IntVar(value=0)
        self.blue = ctk.IntVar(value=0)
        SlidePanel(parent, "red", self.red, 0, 255, update_func=self.convert_to_hex)
        SlidePanel(parent, "green", self.green, 0, 255, update_func=self.convert_to_hex)
        SlidePanel(parent, "blue", self.blue, 0, 255, update_func=self.convert_to_hex)

    def convert_to_hex(self):
        self.color.set('#{:02x}{:02x}{:02x}'.format(self.red.get(), self.green.get(), self.blue.get()))
        print(self.color.get())


class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='green')
        self.pack(expand=True, fill='both')
