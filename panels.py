import customtkinter as ctk


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
    def __init__(self, parent, text, value, low_limit, high_limit):
        super().__init__(parent=parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        self.value_label = ctk.CTkLabel(self, text=round(value.get(), 2))
        self.value_label.grid(column=1, row=0, sticky='E', padx=5)

        ctk.CTkSlider(self,
                      fg_color='grey',
                      variable=value,
                      from_=low_limit,
                      to=high_limit,
                      command=self.update_value
                      ).grid(column=0, row=1, columnspan=2, sticky="ew", padx=5, pady=5)

    def update_value(self, value):
        self.value_label.configure(text=f'{round(value, 2)}')
