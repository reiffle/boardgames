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

def start_minecraft(root, previous_frame, return_to_menu):
    current_frame=clean_frame(root, previous_frame, "Minecraft")
    back_button=back_btn(root, current_frame, return_to_menu)
    back_button.grid(row=0, column=0)
