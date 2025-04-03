import tkinter as tk
from random import randint
from gameboard import clean_frame, back_btn

'''
Minecraft Cell
    clicked
        need left and right click logic
    flagged
    question
    bomb
    number of bombs in vicinity
Setup Board
    get size
    get difficulty or number of bombs
    seed the board
    print the board
Play Game
    check game over
        win - all bombs flagged and all spaces uncovered
        lose - bomb clicked
    if not over
        keep playing
    ask if want to play again
Implement back button for game selection
    '''
gameover=False

class Minesweeper_Cell(tk.Button):
    def __init__(self, master, row, column, **kwargs):
        super().__init__(master, **kwargs)
        self.row=row
        self.column=column
        self.clicked=False
        self.flag=False
        self.question=False
        self.bomb=False
        self.proximity=0
        self.configure(width=2, height=1, command=self.click)
        self.bind("<Button-3>", self.right_click)

    def click(self):
        global gameover
        if (gameover or self.question or self.flag or self.clicked):
            return
        self.clicked=True
        if (self.bomb):
            self.configure(text="*", fg="red")
            gameover=True
            return
        self.configure(text=str(self.proximity), fg="black")

    def right_click(self, event):
        global gameover
        if (self.clicked or gameover):
            return
        if (self.flag):
            self.flag=False
            self.question=True
            self.configure(text="?", fg="green")
            return
        if (self.question):
            self.question=False
            self.configure(text="", fg="black")
            return
        if (not self.question and not self.flag):
            self.flag=True
            self.configure(text="F", fg="blue")    

def new_board(frame, rows, cols):
    cells=[]
    for x in range (rows):
        row=[]
        for y in range (cols):
            cell=Minesweeper_Cell(frame, x, y)
            cell.grid(row=x, column=y)
            row.append(cell)
        cells.append(row)
    place_bombs(cells, rows, cols)

def place_bombs(cells, rows, cols):
    bombs= int(rows*cols*.15) + 1
    while (bombs>0):
        new_x=randint(0, rows-1)
        new_y=randint(0, cols-1)
        if cells[new_x][new_y].bomb:
            continue
        cells[new_x][new_y].bomb=True
        update_proximity(cells, new_x, new_y, rows, cols)
        bombs-=1

def update_proximity(cells, curr_row, curr_col, max_row, max_col):
    for x in range (-1, 2):
        new_x=curr_row+x
        if (new_x<0 or new_x>=max_row):
            continue
        for y in range (-1, 2):
            new_y=curr_col+y
            if (new_y<0 or new_y>=max_col):
                continue
            cells[new_x][new_y].proximity+=1


def start_minesweeper (root, previous_frame, select_return):
    global gameover
    gameover=False
    rows=10
    cols=10
    outer_frame=clean_frame(root, previous_frame, "Minesweeper")
    inner_frame=tk.Frame(outer_frame)
    inner_frame.grid(row=0, column=0)
    new_board(inner_frame, rows, cols)
    back_button=back_btn(root, outer_frame, select_return)
    back_button.grid(row=0, column=1)