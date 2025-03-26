import tkinter as tk

class Window:

    def __init__(self, title="Battleship", width=800, height=600):
        self.title=title #Variables to be allocated by calling program

        self.root=tk.Tk()
        self.root.title(title)
        self.width=width
        self.height=height
        self.root.geometry(f"{width}x{height}")
        self.buttons=[]
        
    def draw_window(self):
        self.root.mainloop()
