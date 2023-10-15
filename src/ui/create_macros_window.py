from tkinter import *


class CreateMacrosWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Окно создания макроса")
        self.geometry("500x500")
        self.label = Label(self, text="Окно создания макроса")
        self.label.pack()
