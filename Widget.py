from tkinter import *


class Game_Widget:
    def __init__(self):
        self.cell_grid = Frame()
        self.mines_left_counter = Label()
        self.countup_timer = Label(text="")
        self.countdown_timer = Label()
        self.communicator = Label()
