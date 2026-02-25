class Cell:
    def __init__(self, value="0"):
        self.value = value
        self.state = "Hidden"

from Cell import *

class Board:
    def __init__(self, grid_height = 0, grid_width = 0):
        #initialising variables
        self.grid_height = grid_height
        self.grid_width = grid_width
        
        #creating grid
        self.grid = [[Cell() for _ in range(grid_width)] for _ in range(grid_height)]        
    

    def show_list(self):
        #reading values and states from cell objects
        self.text_grid_values = [[self.grid[i][j].value for j in range(self.grid_width)] for i in range(self.grid_height)]
        self.text_grid_states = [[self.grid[i][j].state for j in range(self.grid_width)] for i in range(self.grid_height)]
        
        for row in range(self.grid_height):
            print(self.text_grid_values[row])
        for row in range(self.grid_height):
            print(self.text_grid_states[row])

#main code
board = Board(10,10)
board.show_list()

