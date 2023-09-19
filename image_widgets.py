import customtkinter as ctk
from tkinter import filedialog
from tkinter import Canvas
from settings import *


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        # setup
        super().__init__(master= parent)
        self.grid(column=0, columnspan=2, row=0, sticky='nsew', padx=10, pady=10)
        self.import_func = import_func

        ctk.CTkButton(self, text='open image', command=self.open_dialog).pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfilename()
        self.import_func(path)

    def hide(self):
        self.grid_forget()

    def show(self):
        self.grid(column=0, columnspan=2, row=0, sticky='nsew')


class ShowImage(Canvas):
    def __init__(self, parent, place_func):
        super().__init__(master=parent, background=BACKGROUND_COLOR)
        self.grid(row=0, column=1, sticky='nsew')
        self.config(highlightthickness=0, bd=0, relief='ridge')
        self.bind('<Configure>', place_func)

    def hide(self):
        self.delete('all')
        self.grid_forget()


class CloseButton(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(master=parent,
                         text="X",
                         text_color="white",
                         fg_color="transparent",
                         width=40,
                         height=40,
                         hover_color="red",
                         corner_radius=0,
                         command=close_func
                         )
        self.place(relx=0.99, rely=0.01, anchor='ne')

    def hide(self):
        self.place_forget()
