import tkinter as tk  

def clean_frame(root, previous_frame, name=None):
    previous_frame.destroy()
    root.title(name)
    current_frame=tk.Frame(root)
    current_frame.grid(row=0, column=0)
    return current_frame

def back_to_menu(root, current_frame, select_return):
    current_frame.destroy()
    select_return (root, "Select Game")

def back_btn(root, current_frame, select_return):
    return tk.Button(current_frame, text="Back", command=lambda:back_to_menu(root, current_frame, select_return))