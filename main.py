import tkinter as tk
from battleship import play_battleship

def main():

    select_game()

def select_game():

    root=tk.Tk()
    root.geometry("800x800")
    root.title("Boardgames")
    selection_screen=tk.Frame(root)
    selection_screen.grid(row=0, column=0)
    label=tk.Label(selection_screen, text="Please choose your game")
    label.grid(row=0, column=0)
    battleship=tk.Button(selection_screen, text="Battleship", command=lambda: play_battleship(root, selection_screen))
    battleship.grid(row=1,column=0)
    root.mainloop()

main()
