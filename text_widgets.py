import customtkinter as ctk


class TextAdder(ctk.CTkFrame):
    def __init__(self, parent, create_text):
        # setup
        super().__init__(master= parent)
        self.grid(column=0, columnspan=2, row=2, sticky='nsew', padx=10, pady=10)
        self.create_text = create_text

        ctk.CTkButton(self, text='Add Text', command=self.create_text).pack(expand=True)

    def hide(self):
        self.grid_forget()

    def show(self):
        self.grid(column=0, columnspan=2, row=0, sticky='nsew')