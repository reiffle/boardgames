import tkinter as tk
from graphics import Window
from cell import Cell

class Gameboard:
    def __init__(self, row_count=8, column_count=8):
        if type(row_count)!=int or type(column_count)!=int:
            print ("Invalid row or column count")
            return
        if row_count<1 or row_count>26 or column_count<1 or column_count>26:
            print ("Invalid board size")
            return
        self.gameboard=tk.Frame(Window)
        self.gameboard.grid(row=0, column=0)
        cells=[]
        for x in range (10):
            row=[]
            for y in range (10):
                cell=Battle_Cell(self.gameboard, x, y, bg="blue")
                cell.grid(row=x, column=y)
                row.append(cell)
            cells.append(row)

    def shoot (self, x, y):
        button=self.gameboard.buttons[x][y]
        current_text=button.cget("text")
        new_text = ""
        if current_text == "o":
            new_text = "*"
        button.config(bg="gray", disabledforeground="red", text=new_text, state="disabled")

class Battle_Cell(Cell):
    def __init__(self, master, row, col, **kwargs):
        super().__init__(master, row, col, **kwargs)
        self.is_shot = False
        self.configure(command=self.click)


    def click(self):
        if not self.is_shot:
            self.is_shot=True
            if self.empty:
                self.configure(bg="gray", text="O")
            else:
                self.configure(bg="red", text="X")
