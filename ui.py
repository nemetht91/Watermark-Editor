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
from editor_frames import *
from text_widgets import *


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
        self.highlighted_text: TextWidget | None = None
        self.editor_frame: EditorFrame | None = None
        self.image = None

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

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
        self.add_text_button = TextAdder(self, create_text=self.create_text)

    def close_edit(self):
        self.image_shower.hide()
        self.texts.clear()
        self.close_button.hide()
        self.add_text_button.hide()
        self.image_importer.show()
        self.editor_frame.grid_forget()
        self.editor_frame = None

    def place_image(self, event):
        self.canvas_image.resize(event.width, event.height)
        self.image_shower.delete(self.image)
        self.image = self.image_shower.create_image(event.width / 2, event.height / 2, image=self.canvas_image.imageTk)
        self.image_shower.tag_bind(self.image, '<Button-1>', self.click_on_image)
        self.image_shower.tag_lower(self.image)
        if not self.editor_frame:
            self.editor_frame = EditorFrame(self)

    def create_text(self):
        self.unselect_text()
        pos_x, pos_y = self.image_importer.winfo_width()/2, self.image_importer.winfo_height()/2
        new_text = TextWidget(self.image_shower, pos_x, pos_y, self.select_text, self.move_text)
        self.highlight_text(new_text)
        self.texts.append(new_text)

    def select_text(self, text: TextWidget, event):
        self.highlight_text(text)
        self.drag_start(event)

    def highlight_text(self, text: TextWidget):
        self.unselect_text()
        self.highlighted_text = text
        self.editor_frame = TextEditorFrame(self, self.highlighted_text.properties)

    def drag_start(self, event):
        widget = event.widget
        widget.startX, widget.startY = event.x, event.y

    def move_text(self, text: TextWidget, event):
        widget = event.widget
        pos_x, pos_y = event.x-widget.startX, event.y-widget.startY
        text.move(pos_x, pos_y, event)
        widget.startX = event.x
        widget.startY = event.y

    def click_on_image(self, event):
        self.unselect_text()

    def unselect_text(self):
        if self.highlighted_text is None:
            return
        self.highlighted_text.border.hide()
        self.highlighted_text = None
        self.editor_frame.destroy()
        self.editor_frame = EditorFrame(self)

    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title=title, message=message)







