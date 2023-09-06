import tkinter
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
import pyglet
from PIL import Image, ImageTk
from image_widgets import ImageImport, ShowImage
from canvas_image import CanvasImage


BACKGROUND_COLOR = 'black'
MIN_WIDTH = 800
MIN_HEIGHT = 600
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000


class App(ctk.CTk):
    def __init__(self) -> None:
        # setup
        super().__init__()
        self.image_shower: tkinter.Canvas | None = None
        self.canvas_image = CanvasImage(self.show_error)
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

        self.image_importer = ImageImport(self, self.import_image)

        self.mainloop()

    def resize_canvas(self, event):
        if event.widget.widgetName != "toplevel":
            return
        new_width = event.width
        new_height = event.height
        if self.window_width != new_width or self.window_height != new_height:
            self.window_width = new_width
            self.window_height = new_height
            self.canvas.config(width=new_width-100, height=new_height-100)

    def import_image(self, path):
        if not path:
            return
        is_success = self.canvas_image.open(path)
        if not is_success:
            return
        self.image_importer.hide()
        self.image_shower = ShowImage(self, self.place_image)

    def place_image(self, event):
        self.canvas_image.resize(event.width, event.height)
        self.image_shower.delete('all')
        self.image_shower.create_image(event.width / 2, event.height / 2, image=self.canvas_image.imageTk)

    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title=title, message=message)

    @staticmethod
    def browse_files() -> str:
        return filedialog.askopenfilename(
            initialdir='/',
            title="Select an Image",
            filetypes=(("Image", ("*.png*", "*.jpg*")),
                       ("all files", "*.*"))
        )




watermark_editor = App()




