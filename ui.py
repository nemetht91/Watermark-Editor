import tkinter
from tkinter import filedialog, messagebox
from PIL import Image
from image_widgets import *
from canvas_image import CanvasImage
from settings import *
from editor_frames import *
from text_widgets import *
from io import BytesIO



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
        self.image_editor: ImageEditor | None = None
        self.image_canvas_id = None

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
        self.image_editor = ImageEditor(self)
        self.image_canvas_id = self.image_editor.place_image(self.canvas_image)
        self.image_shower = self.image_editor.image_canvas
        self.close_button = CloseButton(self, self.close_edit)
        self.button_frame = ButtonFrame(self, create_text=self.create_text, save_func=self.save_canvas_image)
        self.image_shower.tag_bind(self.image_canvas_id, '<Button-1>', self.click_on_image)
        if not self.editor_frame:
            self.editor_frame = EditorFrame(self)

    def close_edit(self):
        self.image_editor.hide()
        self.texts.clear()
        self.close_button.hide()
        self.button_frame.hide()
        self.image_importer.show()
        self.editor_frame.grid_forget()
        self.editor_frame = None

    def place_image(self, event):
        if self.image_shower is None:
            return
        self.canvas_image.resize(event.width, event.height)
        self.image_shower.delete(self.image_canvas_id)
        self.image_canvas_id = self.image_shower.create_image(event.width / 2, event.height / 2, image=self.canvas_image.imageTk)
        self.image_shower.tag_bind(self.image_canvas_id, '<Button-1>', self.click_on_image)
        self.image_shower.tag_lower(self.image_canvas_id)
        if not self.editor_frame:
            self.editor_frame = EditorFrame(self)

    def create_text(self):
        self.unselect_text()
        pos_x, pos_y = self.image_editor.get_screen_center()
        new_text = TextWidget(self.image_shower, pos_x, pos_y, self.select_text, self.move_text)
        self.highlight_text(new_text)
        self.texts.append(new_text)

    def select_text(self, text: TextWidget, event):
        self.highlight_text(text)
        self.drag_start(event)

    def highlight_text(self, text: TextWidget):
        self.unselect_text()
        self.highlighted_text = text
        self.editor_frame = TextEditorFrame(self, self.highlighted_text.properties, self.delete_text, self.copy_text)

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
        self.highlighted_text.border.clear()
        self.highlighted_text = None
        self.editor_frame.destroy()
        self.editor_frame = EditorFrame(self)

    def delete_text(self):
        if self.highlighted_text is None:
            return
        self.texts.remove(self.highlighted_text)
        self.highlighted_text.delete()
        self.highlighted_text = None
        self.editor_frame.destroy()
        self.editor_frame = EditorFrame(self)

    def copy_text(self):
        if self.highlighted_text is None:
            return
        new_text = TextWidget(self.image_shower, self.highlighted_text.properties.pos_x + 10,
                              self.highlighted_text.properties.pos_y + 10, self.select_text, self.move_text)
        new_text.properties.copy(self.highlighted_text.properties)
        self.unselect_text()
        self.highlight_text(new_text)
        self.texts.append(new_text)

    def save_canvas_image(self):
        self.unselect_text()
        file_path = self.get_file_path()
        eps = self.get_canvas_postscript()
        self.save_to_file(eps, file_path)

    def get_canvas_postscript(self):
        width = self.canvas_image.imageTk.width()
        height = self.canvas_image.imageTk.height()
        return self.image_shower.postscript(colormode='color', width=width, height=height, x=0, y=0)

    @staticmethod
    def save_to_file(eps, file_path):
        if file_path is None or eps is None:
            return
        image = Image.open(BytesIO(bytes(eps, 'ascii')))
        image.save(f"{file_path}.png")

    @staticmethod
    def get_file_path():
        return filedialog.asksaveasfilename(initialfile=f"{IMAGE_PLACE_HOLDER_NAME}",
                                            filetypes=[('image files', '.png')])

    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title=title, message=message)







