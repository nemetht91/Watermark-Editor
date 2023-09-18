import tkinter
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
import pyglet
from PIL import Image, ImageTk
from image_widgets import *
from canvas_image import CanvasImage
from settings import *
from menu import Menu
from text import Text
from text_widgets import TextAdder


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
        self.texts = []
        self.highlighted_text = None

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform= 'a')
        self.columnconfigure(1, weight=6, uniform= 'a')

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
        self.close_button = CloseButton(self, self.close_edit)
        self.menu = Menu(self)
        self.add_text_button = TextAdder(self, create_text=self.create_text)

    def close_edit(self):
        self.image_shower.hide()
        self.close_button.hide()
        self.image_importer.show()

    def place_image(self, event):
        self.canvas_image.resize(event.width, event.height)
        self.image_shower.delete('all')
        self.image_shower.create_image(event.width / 2, event.height / 2, image=self.canvas_image.imageTk)
        self.place_texts()

    def create_text(self):
        text = Text()
        self.texts.append(text)
        self.place_text(text)

    def place_text(self, text: Text):
        text.update_pos(self.image_importer.winfo_width()/2, self.image_importer.winfo_height()/2)
        self.canvas_text = self.image_shower.create_text(text.pos_x,
                                                         text.pos_y,
                                      text=text.text.get(),
                                      fill="red", font=("Courier", 35, "bold"))
        self.image_shower.tag_bind(self.canvas_text, '<Button-1>', self.drag_start)
        self.image_shower.tag_bind(self.canvas_text, '<B1-Motion>', self.move_text)

    def highlight_text(self, event):
        if not self.texts:
            return
        for text in self.texts:
            if abs(event.x - text.pos_x) < 50 and abs(event.y - text.pos_x):
                self.highlighted_text = text

    def drag_start(self, event):
        widget = event.widget
        widget.startX, widget.startY = event.x, event.y

    def move_text(self, event):
        widget = event.widget
        self.image_shower.move(self.canvas_text, event.x-widget.startX, event.y-widget.startY)
        widget.startX = event.x
        widget.startY = event.y
        #self.image_shower.update()

    def place_texts(self):
        if not self.texts:
            return
        for text in self.texts:
            self.place_text(text)



    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title=title, message=message)







