import tkinter as tk
from battleship import play_battleship
from minesweeper import start_minesweeper

def main():
    title="Boardgames"
    root=tk.Tk()
    root.geometry("800x800")
    select_game(root, title)
    root.mainloop()

def select_game(root, title):
    root.title(title)
    selection_screen=tk.Frame(root)
    selection_screen.grid(row=0, column=0)
    label=tk.Label(selection_screen, text="Please choose your game")
    label.grid(row=0, column=0)
    battleship=tk.Button(selection_screen, text="Battleship", command=lambda: play_battleship(root, selection_screen, select_game))
    battleship.grid(row=1,column=0)
    minecraft=tk.Button(selection_screen, text="Minecraft", command=lambda: start_minesweeper(root, selection_screen, select_game))
    minecraft.grid(row=2, column=0)

main()
