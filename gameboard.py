from cell import Cell

class Gameboard:
    def __init__(self, row_count=8, column_count=8):
        if type(row_count)!=int or type(column_count)!=int:
            print ("Invalid row or column count")
            return
        if row_count<1 or row_count>26 or column_count<1 or column_count>26:
            print ("Invalid board size")
            return
        self.gameboard=[]
        self.row_count=row_count
        self.column_count=column_count
        for x in range (self.row_count):
            row=[]
            for y in range (self.column_count):
                row.append(Cell())
            self.gameboard.append(row)

    def __repr__(self):
        printed_board=""
        for row_index in range (self.row_count):
            if row_index==0:
                printed_board+="   "
                for column_index in range (self.column_count):
                    printed_board += " " + chr(ord("A")+column_index)
                printed_board += "\n\n"
            if row_index<10:
                printed_board += " "
            printed_board += f"{row_index} "
            for column_index in range (self.column_count):
                printed_board += f" {self.gameboard[row_index][column_index]}"
            printed_board += ("\n")
        return printed_board
