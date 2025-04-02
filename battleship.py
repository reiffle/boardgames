import tkinter as tk
from random import randint
from gameboard import clean_frame, back_btn

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
def play_battleship(root, previous_frame, select_return):
    current_frame=clean_frame(root, previous_frame, "Battleship")

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
            toggle_board(computer_cells, "normal")
            toggle_board(player_cells, "disabled")
        else:
            display_message("Computer is attacking")
            toggle_board(player_cells, "normal")
            toggle_board(computer_cells, "disabled")
            computer_shot(player_cells, fleet2)
            display_message("Player is attacking")

    #logic for computer play
    def computer_shot(cells, fleet):
        if (not game_over):
            biggest_ship=0
            print ("In computer_shot")
            for ship in range (len(fleet)):
                if (fleet[ship].sunk):
                    print ("First IF")
                    continue
                if (fleet[ship].size>biggest_ship):
                    biggest_ship=fleet[ship].size
                if (fleet[ship].hits!=0 and not fleet[ship].sunk): #if a ship has been hit, but not sunk, fire at it
                    #put in shooting logic
                    ship_val=ship+1
                    print (f"Shooting at {ship_val}")
                    for row in range (len(cells)):
                        for col in range (len(cells[row])):
                            if (not cells[row][col].shot):
                                continue
                            if (cells[row][col].shot):
                                if (not cells[row][col].has_ship==ship_val):
                                    continue
                            shoot_row, shoot_col = lookaround(cells, ship_val, row, col, None)
                            print(f"row: {shoot_row} col: {shoot_col}")
                            cells[shoot_row][shoot_col].click()
                            return
            random_shot(cells, biggest_ship)
            return
            
    #find size of largest remaining ship and take shot covering that area
    def random_shot(cells, length):
        while(True):
            start_x=randint(0,9)
            start_y=randint(0,9)
            place_holder=1
            if (cells[start_x][start_y].shot):
                continue
            while (start_x-place_holder>=0 and not cells[start_x-place_holder][start_y].shot and place_holder<length):
                place_holder+=1
            if (place_holder>=length):
                cells[start_x][start_y].click()
                return
            place_holder-=1
            while (start_x+place_holder<10 and not cells[start_x+place_holder][start_y].shot and place_holder<length):
                place_holder+=1
            if (place_holder>=length):
                cells[start_x][start_y].click()
                return
            place_holder=1
            while (start_y-place_holder>=0 and not cells[start_x][start_y-place_holder].shot and place_holder<length):
                place_holder+=1
            if (place_holder>=length):
                cells[start_x][start_y].click()
                return
            place_holder-=1
            while (start_y+place_holder<10 and not cells[start_x][start_y+place_holder].shot and place_holder<length):
                place_holder+=1
            if (place_holder>=length):
                cells[start_x][start_y].click()
                return


    #helper for computer_shot
    def lookaround(cells, ship_val, row, col, direction):
        print("In lookaround")
        print(f"Start row: {row} Start col:{col}")
        if (row<0 or row>9 or col<0 or col>9): #If out of bounds, return old value
            print('1')
            new_row, new_col=new_coords_opp(row, col, direction)
            return new_row, new_col
        
        if (cells[row][col].shot and not cells[row][col].has_ship==ship_val): #if has already been shot, but didn't have the ship
            print('2')
            print (f"row: {row} col:{col}")
            new_row, new_col=new_coords_opp(row, col, direction)
            print(f"new row:{new_row} new col{new_col}")
            return new_row, new_col

        if (direction==None): #The root position
            print('3')
            UP, DOWN, LEFT, RIGHT=check_direction(cells, row, col)
            if (UP):
                print("up")
                new_row, new_col=new_coords(row, col, "up")
                new_row, new_col=lookaround(cells, ship_val, new_row, new_col, "up")
                if (new_row!=row or new_col!=col):
                    return new_row, new_col
            if (DOWN):
                print("down")
                new_row, new_col=new_coords(row, col, "down")
                new_row, new_col=lookaround(cells, ship_val, new_row, new_col, "down")
                if (new_row!=row or new_col!=col):
                    return new_row, new_col
            if (LEFT):
                print("left")
                new_row, new_col=new_coords(row, col, "left")
                new_row, new_col=lookaround(cells, ship_val, new_row, new_col, "left")
                if (new_row!=row or new_col!=col):
                    return new_row, new_col
            if (RIGHT):
                print("right")
                new_row, new_col=new_coords(row, col, "right")
                new_row, new_col=lookaround(cells, ship_val, new_row, new_col, "right")
                if (new_row!=row or new_col!=col):
                    return new_row, new_col
                
        if (not cells[row][col].shot): #return the coordinates to be shot
            print('4')
            print("shooting")
            return row, col
        print('5')
        new_row, new_col=new_coords(row, col, direction)
        print ("entering recursion")
        new_row, new_col=lookaround(cells, ship_val, new_row, new_col, direction)
        return new_row, new_col


    def check_direction(cells, row, col):
        print("In check_directions")
        UP=False
        DOWN=False
        LEFT=False
        RIGHT=False
        start_cell=cells[row][col]
        #CHECK IF ANYTHING ALREADY ESTABLISHED
        if (row-1>=0 and cells[row-1][col].shot and cells[row-1][col].has_ship==start_cell.has_ship): #CHECK UP
            UP=True
            if (row+1<10 and ((cells[row+1][col].shot and cells[row+1][col].has_ship==start_cell.has_ship) or not cells[row+1][col].shot)):
                DOWN=True
            return UP, DOWN, LEFT, RIGHT
        if (row+1<10 and cells[row+1][col].shot and cells[row+1][col].has_ship==start_cell.has_ship): #CHECK DOWN
            DOWN=True
            if (row-1>=0 and ((cells[row-1][col].shot and cells[row-1][col].has_ship==start_cell.has_ship) or not cells[row-1][col].shot)):
                UP=True
            return UP, DOWN, LEFT, RIGHT
        if (col-1>=0 and cells[row][col-1].shot and cells[row][col-1].has_ship==start_cell.has_ship): #CHECK LEFT
            LEFT=True
            if (col+1<10 and ((cells[row][col+1].shot and cells[row][col+1].has_ship==start_cell.has_ship) or not cells[row][col+1].shot)):
                RIGHT=True
            return UP, DOWN, LEFT, RIGHT
        if (col+1<10 and cells[row][col+1].shot and cells[row][col+1].has_ship==start_cell.has_ship): #CHECK RIGHT
            RIGHT=True
            if (col-1>=0 and ((cells[row][col-1].shot and cells[row][col-1].has_ship==start_cell.has_ship) or not cells[row][col-1].shot)):
                LEFT=True
            return UP, DOWN, LEFT, RIGHT
        #IF NOTHING ESTABLISHED, JUST SAY EVERYTHING NOT SHOT IS FAIR GAME
        if (row-1>=0 and not cells[row-1][col].shot):
            UP=True
        if (row+1<10 and not cells[row+1][col].shot):
            DOWN=True
        if (col-1>=0 and not cells[row][col-1].shot):
            LEFT=True
        if (col+1<10 and not cells[row][col+1].shot):
            RIGHT=True
        return UP, DOWN, LEFT, RIGHT

    def new_coords_opp(row, col, direction):
        if (direction=="up"):
            return row+1, col
        if (direction=="down"):
            return row-1, col
        if (direction=="left"):
            return row, col+1
        if (direction=="right"):
            return row, col-1
        else:
            return row, col
        
    def new_coords(row, col, direction):
        if (direction=="up"):
            return row-1, col
        if (direction=="down"):
            return row+1, col
        if (direction=="left"):
            return row, col-1
        if (direction=="right"):
            return row, col+1
        else:
            return row, col

    fleet1=[Ship("Carrier" , 5, message_callback=display_message), Ship("Battleship" , 4, message_callback=display_message), Ship("Destroyer" , 3, message_callback=display_message), Ship("Submarine" , 3, message_callback=display_message), Ship("Patrol Boat" , 2, message_callback=display_message)]
    fleet2=[Ship("Carrier" , 5, message_callback=display_message), Ship("Battleship" , 4, message_callback=display_message), Ship("Destroyer" , 3, message_callback=display_message), Ship("Submarine" , 3, message_callback=display_message), Ship("Patrol Boat" , 2, message_callback=display_message)]
    board1, computer_cells = setup_board(current_frame, "blue", 0, "Computer", fleet1, message_callback=display_message, switch_turns_callback=switch_turns)
    board2, player_cells = setup_board(current_frame, "green", 2, "Player", fleet2, message_callback=display_message, switch_turns_callback=switch_turns)
    toggle_board(computer_cells, "normal")
    toggle_board(player_cells, "disabled")
    buffer = tk.Label(current_frame, text=" ")
    message_area = tk.Text(current_frame, height=5, width=50, state="disabled")
    back_button = back_btn(root, current_frame, select_return)
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
        #check if end of game - Done