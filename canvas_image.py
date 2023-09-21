import PIL
from PIL import Image, ImageTk
from typing import Callable


class CanvasImage:
    def __init__(self, pop_up_func: Callable[[str, str], None]):
        self.image: Image | None = None
        self.imageTk: ImageTk | None = None
        self.pop_up_func = pop_up_func

    def open(self, path) -> bool:
        try:
            self.image = Image.open(path)
        except FileNotFoundError:
            self.pop_up_func("File import error", "The selected file doesn't exist")
            return False
        except PIL.UnidentifiedImageError:
            self.pop_up_func("File import error", "Image file is not supported.")
            return False
        except [ValueError, TypeError] as e:
            self.pop_up_func("File import error", f"Unknown error occurred: \n{e}")
            return False
        else:
            self.imageTk = ImageTk.PhotoImage(self.image)
            return True

    def resize(self, width, height):
        canvas_ratio = width / height
        image_ratio = self.image.size[0] / self.image.size[1]
        if canvas_ratio > image_ratio:
            image_height = int(height)
            image_width = int(image_height * image_ratio)
        else:
            image_width = int(width)
            image_height = int(width / image_ratio)
        resized_image = self.image.resize((image_width, image_height))
        self.imageTk = ImageTk.PhotoImage(resized_image)
