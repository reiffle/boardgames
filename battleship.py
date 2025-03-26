import tkinter as tk
from random import randint

class Battleship_Cell(tk.Button):
    def __init__(self, master, row, column,fleet_reference=None, info_reference=None, **kwargs):
        super().__init__(master, **kwargs)
        self.row=row
        self.column=column
        self.has_ship=0
        self.shot=False
        self.fleet=fleet_reference
        self.info=info_reference
        self.configure(width=2, height=1, command=self.click)

    def click(self):
        if not self.shot:
            self.shot = True
            if self.has_ship:
                self.configure(bg="red", text="X")
                ship_index=self.has_ship-1
                if self.fleet and 0<=ship_index<len(self.fleet):
                    self.fleet[ship_index].hit()
                    update_info(self.fleet[ship_index], self.info[ship_index+1])
            else:
                self.configure(bg="gray", text="O")

class Ship:
    def __init__(self, name="ship", size=3):
        self.size = size
        self.hits = 0
        self.name = name
        self.sunk = False

    def hit(self):
        self.hits += 1
        print(f"{self.name} has been hit!")
        if self.hits == self.size:
            self.sunk = True
            print(f"{self.name} has been sunk!")

fleet= [Ship("Carrier" , 5), Ship("Battleship" , 4), Ship("Destroyer" , 3), Ship("Submarine" , 3), Ship("Patrol Boat" , 2)]

###Start board creation
def setup_board():
    root=tk.Tk()
    root.title("Battleship")
    fleet1 = [Ship("Carrier" , 5), Ship("Battleship" , 4), Ship("Destroyer" , 3), Ship("Submarine" , 3), Ship("Patrol Boat" , 2)]
    fleet2 = [Ship("Carrier" , 5), Ship("Battleship" , 4), Ship("Destroyer" , 3), Ship("Submarine" , 3), Ship("Patrol Boat" , 2)]
    #Main boards
    game_board1 = tk.Frame(root)
    game_board2 = tk.Frame(root)
    game_board1.grid(row=0, column=0)
    game_board2.grid(row=1, column=0)
    #Ship labels
    fleet_info1 = tk.Frame(root)
    fleet_info2 = tk.Frame(root)
    fleet_info1.grid(row=0, column=1)
    fleet_info2.grid(row=1, column=1)
    #The actual board grids
    info1=init_info(fleet_info1, "blue", fleet1)
    info2=init_info(fleet_info2, "green", fleet2)
    cells1=init_gameboard(game_board1, "blue", fleet1, info1)
    cells2=init_gameboard(game_board2, "green", fleet2, info2)
    for x in range(len(fleet1)):
        place_ship(cells1, fleet1[x].size, x+1)    
    for x in range(len(fleet2)):
        place_ship(cells2, fleet2[x].size, x+1)    
    root.mainloop()

#Make empty board
def init_gameboard(board, background, fleet_reference=None, info_reference=None):
    cells=[]
    for r in range(10):
        row=[]
        for c in range(10):
            cell=Battleship_Cell(board, r, c, fleet_reference=fleet_reference, info_reference=info_reference, bg=background)
            cell.grid(row=r, column=c)
            row.append(cell)
        cells.append(row)
    return cells

def init_info(board, foreground, fleet_reference=None):
    if fleet_reference:
        cells=[]
        row0=[]
        init_cell1=tk.Label(board, text="SHIP NAME", fg=foreground)
        init_cell2=tk.Label(board, text="SIZE", fg=foreground)
        init_cell3=tk.Label(board, text="HITS", fg=foreground)
        init_cell4=tk.Label(board, text="SUNK", fg=foreground)
        init_cell1.grid(row=0, column=0)
        init_cell2.grid(row=0, column=1)
        init_cell3.grid(row=0, column=2)
        init_cell4.grid(row=0, column=3)
        row0.append(init_cell1)
        row0.append(init_cell2)
        row0.append(init_cell3)
        row0.append(init_cell4)
        cells.append(row0)

        for r in range (len(fleet_reference)):
            row = []
            cell1=tk.Label(board, text=fleet_reference[r].name, fg=foreground)
            cell2=tk.Label(board, text=fleet_reference[r].size, fg=foreground)
            cell3=tk.Label(board, text=fleet_reference[r].hits, fg=foreground)
            cell4=tk.Label(board, text=str(fleet_reference[r].sunk), fg=foreground)
            cell1.grid(row=r+1, column=0)
            cell2.grid(row=r+1, column=1)
            cell3.grid(row=r+1, column=2)
            cell4.grid(row=r+1, column=3)
            row.append(cell1)
            row.append(cell2)
            row.append(cell3)
            row.append(cell4)
            cells.append(row)
        return cells

def update_info(ship, info):
    info[2].configure(text=ship.hits)
    if ship.sunk:
        info[3].configure(text=str(ship.sunk))
        for label in info:
            label.configure(fg="red")
            
#Place ship on the board    
def place_ship(cells, ship_size, ship_number):
    while True:
        x = randint(0,9)
        y = randint(0,9)
        ship_direction = randint(0,3) #Up==0, Down==1, Left==2, Right==3
        completed=False
        loop = 0
        while True:
            if ship_direction==0:
                if (y-(ship_size-1)>=0):
                    completed=check_ship (cells, x, y, ship_size, ship_direction, ship_number)
            if ship_direction==1:
                if (x+(ship_size-1)<=9):
                    completed=check_ship (cells, x, y, ship_size, ship_direction, ship_number)
            if ship_direction==2:
                if (y+(ship_size-1)<=9):
                    completed=check_ship (cells, x, y, ship_size, ship_direction, ship_number)
            if ship_direction==3:
                if (x-(ship_size-1)>=0):
                    completed=check_ship (cells, x, y, ship_size, ship_direction, ship_number)
            loop+=1
            if (completed or loop==4):
                break
            ship_direction=(ship_direction+loop)%4
        if (completed):
            break

#Helper function for place_ship    
def check_ship(cells, x, y, size, direction, ship_number):
    if (size==0):
        return True
    if (cells[x][y].has_ship):
        return False
    size-=1 #Less area of ship to check
    # Move one space
    x1=x
    y1=y
    if (direction==0): y-=1
    elif (direction==1): x+=1
    elif (direction==2): y+=1
    else: x-=1
    #End Move
    if check_ship(cells, x, y, size, direction, ship_number):
        cells[x1][y1].has_ship=ship_number
        return True
    return False
###End Board creation

def play_battleship():
    setup_board()
    #setup board
        #create blank boards -- Done
            #computer -- Done
            #person -- Done
        #place ships
            #computer
            #person
    #play game
        #shoot target
        #check if already shot
        #check if occupied by ship
        #check if ship sunk
        #check if end of game
'''
class Player:
    def __init__ (self, name="Computer"):
        self.name = name
        self.board = GameBoard(10, 10)
        self.fleet = []

    '''