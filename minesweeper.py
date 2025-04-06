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
gameboard=[]
total_cells=0
total_cells_uncovered=0
total_bombs=0
bombs_flagged=0
flag_count=tk.Label

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
        global total_cells_uncovered
        global bombs_flagged
        global total_cells

        if (gameover or self.question or self.flag or self.clicked):
            return
        self.clicked=True
        total_cells_uncovered+=1
        if (self.bomb):
            self.configure(text="*", bg="red", fg="white")
            gameover=True
            gameover_routine()
            return
        self.configure(text=str(self.proximity), fg="black")
        clear_empty(self.row, self.column)
        gameover_routine()

    def right_click(self, event):
        global gameover
        global bombs_flagged
        global flag_count
        global total_bombs
        global total_cells_uncovered
        global total_cells

        if (self.clicked or gameover):
            return
        if (self.flag):
            self.flag=False
            self.question=True
            self.configure(text="?", fg="green")
            bombs_flagged-=1
            flag_count.configure(text=f"Bombs remaining: {total_bombs-bombs_flagged}")
            return
        if (self.question):
            self.question=False
            self.configure(text="", fg="black")
            return
        if (not self.question and not self.flag):
            self.flag=True
            self.configure(text="F", fg="blue")
            bombs_flagged+=1
            flag_count.configure(text=f"Bombs remaining: {total_bombs-bombs_flagged}")
            gameover_routine()

def clear_empty(row, col):
    global gameboard
    if gameboard[row][col].proximity!=0: return #Go back if ther are bombs nearby
    total_row_size=len(gameboard)
    total_col_size=len(gameboard[0])
    for x in range(-1,2):
        new_row=row+x
        if (new_row<0 or new_row>=total_row_size):
            continue
        for y in range (-1,2):
            new_col=col+y
            if (new_col<0 or new_col>=total_col_size):
                continue
            cell=gameboard[new_row][new_col]
            if (not cell.clicked and not cell.flag and not cell.question):
                cell.click()

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
    return cells

def place_bombs(cells, rows, cols):
    global total_bombs
    bombs = int(rows*cols*.15) + 1
    total_bombs=bombs
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

def gameover_routine():
    global gameboard
    global gameover
    global bombs_flagged
    global total_cells_uncovered

    row=len(gameboard)
    col=len(gameboard[0])

    total_cells=row*col

    if (gameover==True):
        print ("You lose")
        for x in range (row):
            for y in range (col):
                if (not gameboard[x][y].clicked and gameboard[x][y].bomb):
                    gameboard[x][y].configure(text="*", fg="red")
    print (f"total cells: {total_cells} bombs flagged: {bombs_flagged} cells:clicked: {total_cells_uncovered}")
    if (total_cells==bombs_flagged+total_cells_uncovered):
        gameover=True
        print("You win")
    else:
        return

def start_minesweeper (root, previous_frame, select_return):
    global gameover
    global gameboard
    global total_bombs
    global bombs_flagged
    global flag_count
    global total_cells
    global total_cells_uncovered

    gameover=False
    gameboard=[]
    total_cells=0
    total_cells_uncovered=0
    total_bombs=0
    bombs_flagged=0
    flag_count=tk.Label

    rows=10
    cols=10
    outer_frame=clean_frame(root, previous_frame, "Minesweeper")
    inner_frame=tk.Frame(outer_frame)
    inner_frame.grid(row=0, column=0)
    gameboard=new_board(inner_frame, rows, cols)
    back_button=back_btn(root, outer_frame, select_return)
    back_button.grid(row=1, column=0, sticky="w")
    flag_count=tk.Label(outer_frame, text=f"Bombs remaining: {total_bombs-bombs_flagged}")
    flag_count.grid(row=0, column=1, sticky="n")