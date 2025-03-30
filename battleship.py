import tkinter as tk
from random import randint

game_over=False

class Battleship_Cell(tk.Button):
    def __init__(self, master, row, column, name=None, fleet_reference=None, info_reference=None, message_callback=None, switch_turns_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.row=row
        self.column=column
        self.has_ship=0
        self.shot=False
        self.fleet=fleet_reference
        self.info=info_reference
        self.message_callback=message_callback
        self.switch_turns=switch_turns_callback
        self.name=name
        self.configure(width=2, height=1, command=self.click)

    def click(self):
        if (game_over):
            return
        if not self.shot:
            self.switch_turns()
            self.shot = True
            self.message_callback(f"X:{self.column}, Y:{self.row}")
            if self.has_ship:
                self.configure(bg="red", text="X")
                ship_index=self.has_ship-1
                if self.fleet and 0<=ship_index<len(self.fleet):
                    self.fleet[ship_index].hit()
                    update_info(self.fleet[ship_index], self.info[ship_index+1])
                    self.check_gameover()
            else:
                self.configure(bg="gray", text="O")
                self.message_callback("Miss!")

    def check_gameover(self):
        global game_over
        for ship in (self.fleet):
            if (not ship.sunk):
                return
        if self.message_callback:
            self.message_callback(f"{self.name} has no ships. Opponent wins!")
            game_over=True
            return
        print("Gameover")
        game_over=True
        return

class Ship:
    def __init__(self, name="ship", size=3, message_callback=None):
        self.size = size
        self.hits = 0
        self.name = name
        self.sunk = False
        self.message_callback = message_callback

    def hit(self):
        self.hits += 1
        if self.message_callback:
            self.message_callback(f"{self.name} has been hit!")
        else:
            print(f"{self.name} has been hit!")
        if self.hits == self.size:
            self.sunk = True
            if self.message_callback:
                self.message_callback(f"{self.name} has been sunk!")
            else:
                print(f"{self.name} has been sunk!")

###Start board creation
def setup_board(frame, hue, row, name, fleet, message_callback=None, switch_turns_callback=None):

    board_container=tk.Frame(frame)
    fleet1 = fleet
    #Main boards
    game_board1 = tk.Frame(board_container)
    game_board1.grid(row=row, column=0)
    #Ship labels
    fleet_info1 = tk.Frame(board_container)
    fleet_info1.grid(row=row, column=1)
    #The actual board grids
    info1=init_info(fleet_info1, hue, fleet1)
    cells1=init_gameboard(game_board1, hue, name, fleet1, info1, message_callback, switch_turns_callback=switch_turns_callback)
    for x in range(len(fleet1)):
        place_ship(name, cells1, fleet1[x].size, x+1)
    board_container.grid(row=row, column=0)
    return board_container, cells1    

#Make empty board
def init_gameboard(board, background, name, fleet_reference=None, info_reference=None, message_callback=None, switch_turns_callback=None):
    cells=[]
    for r in range(10):
        row=[]
        for c in range(10):
            cell=Battleship_Cell(board, r, c, name, fleet_reference=fleet_reference, info_reference=info_reference, bg=background, message_callback=message_callback, switch_turns_callback=switch_turns_callback)
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

def toggle_board(cells, state):
    for row in cells:
        for cell in row:
            if not cell.shot:
                cell.configure(state=state)
            
#Place ship on the board    
def place_ship(name, cells, ship_size, ship_number):
    while True:
        x = randint(0,9)
        y = randint(0,9)
        ship_direction = randint(0,3) #Up==0, Down==1, Left==2, Right==3
        completed=False
        loop = 0
        while True:
            if ship_direction==0:
                if (y-(ship_size-1)>=0):
                    completed=check_ship (name, cells, x, y, ship_size, ship_direction, ship_number)
            if ship_direction==1:
                if (x+(ship_size-1)<=9):
                    completed=check_ship (name, cells, x, y, ship_size, ship_direction, ship_number)
            if ship_direction==2:
                if (y+(ship_size-1)<=9):
                    completed=check_ship (name, cells, x, y, ship_size, ship_direction, ship_number)
            if ship_direction==3:
                if (x-(ship_size-1)>=0):
                    completed=check_ship (name, cells, x, y, ship_size, ship_direction, ship_number)
            loop+=1
            if (completed or loop==4):
                break
            ship_direction=(ship_direction+loop)%4
        if (completed):
            break

#Helper function for place_ship    
def check_ship(name, cells, x, y, size, direction, ship_number):
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
    if check_ship(name, cells, x, y, size, direction, ship_number):
        cells[x1][y1].has_ship=ship_number
        if name != "Computer":
            cells[x1][y1].config(bg="gray30", text=str(ship_number))
        return True
    return False
###End Board creation
def back_to_menu(current_frame):
    current_frame.destroy()
    from main import select_game
    select_game()

def play_battleship(root, previous_frame):
    previous_frame.destroy()
    root.title("Battleship")
    current_frame=tk.Frame(root)
    current_frame.grid(row=0, column=0)

    player_turn=True

    def display_message(message):
        message_area.config(state="normal")
        message_area.insert(tk.END, message + "\n", "left")
        message_area.see(tk.END)
        message_area.config(state="disabled")

    def switch_turns():
        nonlocal player_turn
        player_turn=not player_turn
        if player_turn:
            display_message("Computer is attacking")
            toggle_board(computer_cells, "normal")
            toggle_board(player_cells, "disabled")
        else:
            display_message("Player is attacking")
            toggle_board(player_cells, "normal")
            toggle_board(computer_cells, "disabled")

    fleet1=[Ship("Carrier" , 5, message_callback=display_message), Ship("Battleship" , 4, message_callback=display_message), Ship("Destroyer" , 3, message_callback=display_message), Ship("Submarine" , 3, message_callback=display_message), Ship("Patrol Boat" , 2, message_callback=display_message)]
    fleet2=[Ship("Carrier" , 5, message_callback=display_message), Ship("Battleship" , 4, message_callback=display_message), Ship("Destroyer" , 3, message_callback=display_message), Ship("Submarine" , 3, message_callback=display_message), Ship("Patrol Boat" , 2, message_callback=display_message)]
    board1, computer_cells = setup_board(current_frame, "blue", 0, "Computer", fleet1, message_callback=display_message, switch_turns_callback=switch_turns)
    board2, player_cells = setup_board(current_frame, "green", 2, "Player", fleet2, message_callback=display_message, switch_turns_callback=switch_turns)
    toggle_board(computer_cells, "normal")
    toggle_board(player_cells, "disabled")
    buffer = tk.Label(current_frame, text=" ")
    message_area = tk.Text(current_frame, height=5, width=50, state="disabled")
    back_button = tk.Button(current_frame, text="Back", command=lambda: back_to_menu(root))
    board1.grid(row=0, column=0)
    buffer.grid(row=1,column=0)
    board2.grid(row=2, column=0)
    message_area.grid(row=3, column=0, sticky="w")
    back_button.grid(row=4, column=0)

    #root.mainloop()
    #setup board
        #create blank boards -- Done
            #computer -- Done
            #person -- Done
        #place ships
            #computer -- Done
            #person
    #play game
        #shoot target
        #check if already shot - Done
        #check if occupied by ship - Done
        #check if ship sunk - Done
        #check if end of game