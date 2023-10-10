import customtkinter as ctk
from tkinter import filedialog
from tkinter import Canvas
from settings import *
from canvas_image import CanvasImage


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


class ImageEditor:
    def __init__(self, parent):
        self.image_canvas = Canvas(parent, background=BACKGROUND_COLOR)
        self.image_canvas.grid(column=1, row=0, sticky="")
        self.vertical_scroll = ctk.CTkScrollbar(parent, orientation="vertical", command=self.image_canvas.yview)
        self.vertical_scroll.grid(column=2, row=0, sticky="ns")

        self.horizontal_scroll = ctk.CTkScrollbar(parent, orientation="horizontal", command=self.image_canvas.xview)
        self.horizontal_scroll.grid(column=1, row=1, sticky="ew")

        self.image_canvas.configure(xscrollcommand=self.horizontal_scroll.set, yscrollcommand=self.vertical_scroll.set)
        self.image_canvas_id = None

    def place_image(self, image: CanvasImage):
        self.image_canvas.configure(width=image.imageTk.width(), height=image.imageTk.height())
        self.image_canvas_id = self.image_canvas.create_image(
            image.imageTk.width() / 2, image.imageTk.height() / 2, image=image.imageTk)
        self.image_canvas.bind('<Configure>',
                               lambda e: self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all")))
        return self.image_canvas_id

    def get_screen_center(self):
        pos_x0 = self.image_canvas.canvasx(0)
        pos_y0 = self.image_canvas.canvasy(0)
        pos_x1 = self.image_canvas.canvasx(self.image_canvas.winfo_width())
        pos_y1 = self.image_canvas.canvasy(self.image_canvas.winfo_height())
        pos_x = pos_x0 + (pos_x1 - pos_x0) / 2
        pos_y = pos_y0 + (pos_y1 - pos_y0) / 2
        return pos_x, pos_y

    def hide(self):
        self.image_canvas.delete('all')
        self.image_canvas.grid_forget()
        self.vertical_scroll.grid_forget()
        self.horizontal_scroll.grid_forget()


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


class ImageSaver(ctk.CTkFrame):
    def __init__(self, parent, save_func):
        # setup
        super().__init__(master=parent)
        self.grid(column=2, columnspan=2, row=3, sticky='nsew', padx=10, pady=10)

        ctk.CTkButton(self, text='Save', command=save_func).pack(expand=True)

    def hide(self):
        self.grid_forget()

    def show(self):
        self.grid(column=2, columnspan=2, row=3, sticky='nsew', padx=10, pady=10)