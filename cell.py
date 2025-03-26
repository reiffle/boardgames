import tkinter as tk

class Cell(tk.Button):
    def __init__(self, master, row, col, **kwargs):
        super().__init__(master, **kwargs)
        self.row=row
        self.col=col
        self.empty = True

        