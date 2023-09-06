from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog
import tkinter.font as tkfont
import pyglet
from PIL import Image, ImageTk
from image_widgets import ImageImport

BACKGROUND_COLOR = 'black'
MIN_WIDTH = 800
MIN_HEIGHT = 600
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000


class App(ctk.CTk):
    def __init__(self) -> None:
        # setup
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.title('Watermark Editor')
        self.geometry('1000x600')
        self.minsize(width=MIN_WIDTH, height=MIN_HEIGHT)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        ImageImport(self, self.open_image)
        # self.main_menu = tk.Menu(self)
        # self.config_main_menu()
        self.image = None
        # self.canvas = self.create_canvas()
        # self.canvas_image = None
        self.mainloop()

    def create_canvas(self):
        canvas = ctk.Canvas(self, width=self.window_width-100, height=self.window_height-100)
        canvas.config(background="white", border=1, borderwidth=2)
        canvas.grid(row=0, column=0)
        return canvas

    def resize_canvas(self, event):
        if event.widget.widgetName != "toplevel":
            return
        new_width = event.width
        new_height = event.height
        if self.window_width != new_width or self.window_height != new_height:
            self.window_width = new_width
            self.window_height = new_height
            self.canvas.config(width=new_width-100, height=new_height-100)

    def open_image(self):
        file_name = self.browse_files()
        if not file_name:
            return
        self.image = ImageTk.PhotoImage(Image.open(file_name))
        self.add_image()

    def add_image(self):
        if not self.image:
            return
        #self.canvas.config(width=self.image.width(), height=self.image.height())
        x_pos = self.canvas.winfo_width() / 2
        y_pos = self.canvas.winfo_height() / 2
        self.canvas_image = self.canvas.create_image(x_pos, y_pos, image=self.image)

    def move(self, event):
        if self.canvas_image is None:
            return
        self.canvas.move(self.canvas_image, event.x, event.y)

    def save(self):
        ...

    def new_project(self):
        ...

    @staticmethod
    def browse_files() -> str:
        return filedialog.askopenfilename(
            initialdir='/',
            title="Select an Image",
            filetypes=(("Image", ("*.png*", "*.jpg*")),
                       ("all files", "*.*"))
        )




watermark_editor = App()




