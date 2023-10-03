import customtkinter as ctk
from PIL import ImageColor


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='grey')
        self.pack(fill='x', pady=4, ipady=8)


class TextBoxPanel(Panel):
    def __init__(self, parent, text, value):
        super().__init__(parent=parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        self.entry = ctk.CTkEntry(self,
                                  placeholder_text='Your Text',
                                  textvariable=value,
                                  )
        self.entry.grid(column=0, row=1, columnspan=2, sticky="ew", padx=5, pady=5)


class SlidePanel(Panel):
    def __init__(self, parent, text, value, low_limit, high_limit, update_func=None):
        super().__init__(parent=parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        self.value_label = ctk.CTkLabel(self, text=round(value.get(), 2))
        self.value_label.grid(column=1, row=0, sticky='E', padx=5)
        self.update_func = update_func

        ctk.CTkSlider(self,
                      fg_color='grey',
                      variable=value,
                      from_=low_limit,
                      to=high_limit,
                      command=self.update_value
                      ).grid(column=0, row=1, columnspan=2, sticky="ew", padx=5, pady=5)

    def update_value(self, value):
        self.value_label.configure(text=f'{round(value, 2)}')


class ColorPanel(Panel):
    def __init__(self, parent, value):
        super().__init__(parent=parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.color = value
        rgb = self.get_to_rgb()
        self.red = ctk.IntVar(value=rgb[0])
        self.green = ctk.IntVar(value=rgb[1])
        self.blue = ctk.IntVar(value=rgb[2])

        ctk.CTkLabel(self, text="Color").grid(column=0, row=0, sticky='W', padx=5)
        self.color_value_label = ctk.CTkLabel(self, text=self.color.get())
        self.color_value_label.grid(column=1, row=0, sticky='E', padx=5)
        ctk.CTkLabel(self, text="R").grid(column=0, row=1, sticky='W', padx=5)
        self.red_value_label = ctk.CTkLabel(self, text=round(self.red.get()))
        self.red_value_label.grid(column=1, row=1, sticky='E', padx=5)
        ctk.CTkSlider(self,
                      fg_color='grey',
                      variable=self.red,
                      from_=0,
                      to=255,
                      command=self.update_color
                      ).grid(column=0, row=2, columnspan=2, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(self, text="G").grid(column=0, row=3, sticky='W', padx=5)
        self.green_value_label = ctk.CTkLabel(self, text=round(self.green.get()))
        self.green_value_label.grid(column=1, row=3, sticky='E', padx=5)
        ctk.CTkSlider(self,
                      fg_color='grey',
                      variable=self.green,
                      from_=0,
                      to=255,
                      command=self.update_color
                      ).grid(column=0, row=4, columnspan=2, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(self, text="B").grid(column=0, row=5, sticky='W', padx=5)
        self.blue_value_label = ctk.CTkLabel(self, text=round(self.blue.get()))
        self.blue_value_label.grid(column=1, row=5, sticky='E', padx=5)
        ctk.CTkSlider(self,
                      fg_color='grey',
                      variable=self.blue,
                      from_=0,
                      to=255,
                      command=self.update_color
                      ).grid(column=0, row=6, columnspan=2, sticky="ew", padx=5, pady=5)
        self.update_color(None)

    def update_color(self, value):
        self.convert_to_hex()
        self.update_labels()

    def convert_to_hex(self):
        self.color.set('#{:02x}{:02x}{:02x}'.format(self.red.get(), self.green.get(), self.blue.get()))

    def update_labels(self):
        self.color_value_label.configure(text=self.color.get())
        self.red_value_label.configure(text=f'{round(self.red.get())}')
        self.green_value_label.configure(text=f'{round(self.green.get())}')
        self.blue_value_label.configure(text=f'{round(self.blue.get())}')

    def get_to_rgb(self):
        return ImageColor.getrgb(self.color.get())


class DoubleButtonPanel(Panel):
    def __init__(self, parent, btn1_name, btn1_func, btn2_name, btn2_func):
        super().__init__(parent=parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.button1 = ctk.CTkButton(self, text=btn1_name, command=btn1_func)
        self.button1.grid(column=0, row=0, sticky="e", padx=5, pady=5)

        self.button2 = ctk.CTkButton(self, text=btn2_name, command=btn2_func)
        self.button2.grid(column=1, row=0, sticky="w", padx=5, pady=5)