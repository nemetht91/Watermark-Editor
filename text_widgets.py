import customtkinter as ctk
from textproperties import TextProperties
from math import sin, cos, pi


class TextAdder(ctk.CTkFrame):
    def __init__(self, parent, create_text):
        # setup
        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=3, sticky='nsew', padx=10, pady=10)
        self.create_text = create_text

        ctk.CTkButton(self, text='Add Text', command=self.create_text).pack(expand=True)

    def hide(self):
        self.grid_forget()

    def show(self):
        self.grid(column=0, columnspan=2, row=0, sticky='nsew')


class TextWidget:
    def __init__(self, canvas: ctk.CTkCanvas, pos_x, pos_y, highlight_func, move_func):
        self.parent_canvas = canvas
        self.properties = TextProperties(pos_x, pos_y, self.update)
        self.border = BorderWidget(canvas, self)
        self.canvas_id = None
        self.create()
        self.highlight_func = highlight_func
        self.move_func = move_func

    def create(self):
        self.canvas_id = self.parent_canvas.create_text(
            self.properties.pos_x,
            self.properties.pos_y,
            text=self.properties.text.get(),
            fill=self.properties.color.get(),
            font=(self.properties.font.get(), self.properties.size.get(), 'bold')
        )
        self.set_angle()
        self.create_binds()
        self.border.draw()

    def create_binds(self):
        self.parent_canvas.tag_bind(self.canvas_id, '<Button-1>', self.highlight)
        self.parent_canvas.tag_bind(self.canvas_id, '<B1-Motion>', self.move_trigger)

    def highlight(self, event):
        self.highlight_func(self, event)
        self.border.draw()

    def move_trigger(self, event):
        self.move_func(self, event)

    def move(self, pos_x, pos_y, event):
        self.parent_canvas.move(self.canvas_id, pos_x, pos_y)
        self.border.move(pos_x, pos_y)
        self.properties.update_pos(event.x, event.y)

    def set_angle(self):
        self.parent_canvas.itemconfig(
            self.canvas_id,
            angle=self.properties.rotation.get()
        )

    def update(self, var, index, mode):
        self.parent_canvas.itemconfig(
            self.canvas_id,
            text=self.properties.text.get(),
            angle=self.properties.rotation.get(),
            font=(self.properties.font.get(), self.properties.size.get(), 'bold'),
            fill=self.properties.color.get()
        )
        self.border.update()

    def get_vertical_bbox(self):
        coords = self.parent_canvas.coords(self.canvas_id)
        vertical_text = self.parent_canvas.create_text(coords,
                                                       text=self.properties.text.get(),
                                                       font=(self.properties.font.get(), self.properties.size.get(),
                                                             'bold')
                                                       )
        bbox = self.parent_canvas.bbox(vertical_text)
        self.parent_canvas.delete(vertical_text)
        return bbox

    def delete(self):
        self.border.clear()
        self.parent_canvas.delete(self.canvas_id)
        self.canvas_id = None


class BorderWidget:
    def __init__(self, canvas: ctk.CTkCanvas, parent_text: TextWidget):
        self.parent_canvas = canvas
        self.parent_text = parent_text
        self.canvas_id = None
        self.corners = []

    def create_shape(self):
        bbox = self.parent_text.get_vertical_bbox()
        self.corners.clear()
        self.corners.append([bbox[0], bbox[1]])
        self.corners.append([bbox[2], bbox[1]])
        self.corners.append([bbox[2], bbox[3]])
        self.corners.append([bbox[0], bbox[3]])
        self.set_angle()

    def draw(self):
        self.create_shape()
        if self.canvas_id:
            self.clear()
        self.canvas_id = self.parent_canvas.create_polygon(self.corners, outline='blue', fill='')
        self.parent_canvas.tag_raise(self.parent_text.canvas_id, self.canvas_id)

    def clear(self):
        self.parent_canvas.delete(self.canvas_id)
        self.canvas_id = None

    def move(self, pos_x, pos_y):
        self.parent_canvas.move(self.canvas_id, pos_x, pos_y)

    def update(self):
        self.clear()
        self.draw()

    def set_angle(self):
        angle = -self.parent_text.properties.rotation.get()
        center = self.get_center()
        for i, corner in enumerate(self.corners):
            self.corners[i] = self.rotate_corner(corner[0], corner[1], angle, center)

    def rotate_corner(self, x, y, angle, center):
        x -= center[0]
        y -= center[1]
        x_rotated = x * cos(angle / 180 * pi) - y * sin(angle / 180 * pi) + center[0]
        y_rotated = x * sin(angle / 180 * pi) + y * cos(angle / 180 * pi) + center[1]
        return x_rotated, y_rotated

    def get_center(self):
        corner_1 = self.corners[0]
        corner_2 = self.corners[2]
        return [(corner_2[0] + corner_1[0])/2, (corner_1[1] + corner_2[1])/2]
