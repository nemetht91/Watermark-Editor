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
from textproperties import TextProperties
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
        self.highlighted_text: TextProperties | None = None
        self.highlight_border = None
        self.editor_frame: EditorFrame | None = None

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
        self.image_shower.delete('all')
        image = self.image_shower.create_image(event.width / 2, event.height / 2, image=self.canvas_image.imageTk)
        self.image_shower.tag_bind(image, '<Button-1>', self.click_on_image)
        self.place_texts()
        self.editor_frame = EditorFrame(self)

    def create_text(self):
        self.unselect_text()
        pos_x, pos_y = self.image_importer.winfo_width()/2, self.image_importer.winfo_height()/2
        new_text = TextProperties(pos_x, pos_y)
        self.place_text(new_text)
        self.texts.append(new_text)
        self.highlight_text(new_text)

    def place_text(self, text: TextProperties):
        text.canvas_id = self.image_shower.create_text(text.pos_x, text.pos_y,
                                                       text=text.text.get(),
                                                       fill="red", font=("Courier", 35, "bold"))
        self.image_shower.tag_bind(text.canvas_id, '<Button-1>', self.select_text)
        self.image_shower.tag_bind(text.canvas_id, '<B1-Motion>', self.move_text)

    def select_text(self, event):
        self.unselect_text()
        text = self.identify(event)
        if text is None:
            return
        self.highlight_text(text)
        self.drag_start(event)

    def identify(self, event):
        if not self.texts:
            return
        canvas_id = self.image_shower.find_overlapping(event.x, event.y, event.x, event.y)
        for text in self.texts:
            if text.canvas_id == canvas_id[1]:
                return text
        return None

    def highlight_text(self, text: TextProperties):
        self.highlighted_text = text
        self.highlighted_text.add_text_trace(self.update_text)
        self.create_text_border()
        self.image_shower.tag_raise(self.highlighted_text.canvas_id, self.highlight_border)
        self.editor_frame = TextEditorFrame(self, self.highlighted_text)

    def create_text_border(self):
        bbox = self.image_shower.bbox(self.highlighted_text.canvas_id)
        self.highlight_border = self.image_shower.create_rectangle(bbox, outline="red")

    def drag_start(self, event):
        widget = event.widget
        widget.startX, widget.startY = event.x, event.y

    def move_text(self, event):
        if self.highlighted_text is None:
            return
        widget = event.widget
        pos_x, pos_y = event.x-widget.startX, event.y-widget.startY
        self.image_shower.move(self.highlighted_text.canvas_id, pos_x, pos_y)
        self.image_shower.move(self.highlight_border, pos_x, pos_y)
        self.highlighted_text.update_pos(event.x, event.y)
        widget.startX = event.x
        widget.startY = event.y

    def click_on_image(self, event):
        self.unselect_text()

    def unselect_text(self):
        if self.highlighted_text:
            self.highlighted_text.remove_text_trace()
        self.highlighted_text = None
        self.remove_text_border()
        self.editor_frame = EditorFrame(self)

    def place_texts(self):
        if not self.texts:
            return
        for text in self.texts:
            self.place_text(text)

    def remove_text_border(self):
        self.image_shower.delete(self.highlight_border)
        self.highlight_border = None

    def update_text(self, var, index, mode):
        self.image_shower.itemconfig(
            self.highlighted_text.canvas_id,
            text=self.highlighted_text.text.get(),
        )
        self.remove_text_border()
        self.create_text_border()

    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title=title, message=message)







