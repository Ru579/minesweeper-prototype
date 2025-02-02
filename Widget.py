from tkinter import *

class Widget:
    def __init__(self):
        self.cell_grid = Frame()
        self.mines_left_counter = Label()
        self.timer = Label()
        self.communicator = Label()