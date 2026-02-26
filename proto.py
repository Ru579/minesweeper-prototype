from Cell import Cell
from random import randint

class Board:
    def __init__(self, grid_height, grid_width, no_of_mines):
        #initialising variables
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.no_of_mines = no_of_mines
        self.flags_left = 0
        self.not_enough_flags = False
        self.game_started = False
        self.game_over = False
        
        #creating grid
        self.grid = [[Cell() for _ in range(grid_width)] for _ in range(grid_height)]
    
    def place_mines(self):
        for i in range(self.no_of_mines):
            while True:
                #randomly selecting a coordinate
                x = randint(0, (self.grid_height - 1))
                y = randint(0, (self.grid_width - 1))
                if self.grid[x][y].value != "*":
                    self.grid[x][y].value = "*"
                    break
    
    def calculate_cell_numbers(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.grid[i][j].value != "*":
                    # setting the value of the cell to the number of mines around it
                    self.grid[i][j].value = self.count_surroundings(i, j, lambda cell: cell.value == "*", edge_wrap = False)
    
    def count_surroundings(self, x, y, predicate, edge_wrap):
        count = 0
        for cell in self.get_surrounding_cells(x, y, edge_wrap):
            if predicate(cell):
                count += 1
        return str(count)
    
    def get_surrounding_cells(self, x, y, edge_wrap):
        cells = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if self.in_bounds(i, j):
                    cells.append(self.grid[i][j])
                elif edge_wrap:
                    #resolving out of bounds x coordinates
                    if i<0:
                        i = self.grid_height - 1
                    elif i>self.grid_height-1:
                        i = 0
                    #resolving out of bounds y coordinates
                    if j<0:
                        j = self.grid_width-1
                    if j>self.grid_width-1:
                        j = 0
                    cells.append(self.grid[i][j])
        return cells

    def in_bounds(self, x, y):
        if 0 <= x < self.grid_height and 0 <= y < self.grid_width:
            return True
        return False
        
    def open_cell(self, x, y):
        if self.grid[x][y].state == "Hidden":
            self.grid[x][y].state = "Revealed"

            if self.grid[x][y].value == "*":
                self.game_over = True
            elif self.grid[x][y].value == "0":
                self.auto_reveal_surroundings(x, y)
    
    def auto_reveal_surroundings(self, x, y):
        #iterating through surrounding cells and revealing them
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if self.in_bounds(i, j) and self.grid[i][j].state == "Hidden":
                    self.grid[i][j].state = "Revealed"

                    if self.grid[i][j].value == "*":
                        self.game_over = True
                    
                    # if any of the surrounding cells are 0 cells, auto reveal their surroundings
                    if self.grid[i][j].value == "0":
                        self.auto_reveal_surroundings(i,j)

    
    def flag_cell(self, x, y):
        if self.grid[x][y].state == "Hidden":
            if self.flags_left > 0:
                self.grid[x][y].state = "Flagged" # flagging the cell if there are enough flags left
            else:
                self.not_enough_flags = True
        elif self.grid[x][y].state == "Flagged":
            self.grid[x][y].state = "Hidden"
    
    def confuse_cell(self, x, y):
        if self.grid[x][y].state != "Revealed":
            if self.grid[x][y].state != "Confused":
                self.grid[x][y].state = "Confused"
            elif self.grid[x][y].state == "Confused":
                self.grid[x][y].state = "Hidden"


    def show_grid(self):
        #reading values and states from cell objects
        self.text_grid_values = [[self.grid[i][j].value for j in range(self.grid_width)] for i in range(self.grid_height)]
        self.text_grid_states = [[self.grid[i][j].state for j in range(self.grid_width)] for i in range(self.grid_height)]
        
        for row in range(self.grid_height):
            print(self.text_grid_values[row])
        for row in range(self.grid_height):
            print(self.text_grid_states[row])
    
    def user_interation(self):
        player_active = True
        while player_active:
            game_action = int(input("(1): Open Cell\n(2): Flag Cell\n(3): Confuse Cell\n(4): End Interaction"))
            if game_action != 4:
                x_coordinate = int(input("Enter x coordinate:"))
                y_coordinate = int(input("Enter y coordinate:"))
            if game_action == 1:
                self.open_cell(x_coordinate, y_coordinate)
                if self.game_over:
                    print("GAME OVER")
            elif game_action == 2:
                self.flag_cell(x_coordinate, y_coordinate)
            elif game_action == 3:
                self.confuse_cell(x_coordinate, y_coordinate)
            elif game_action == 4:
                player_active = False


#main code
board = Board(3,3, 2)
board.flags_left = 2
board.place_mines()
board.calculate_cell_numbers()
board.show_grid()
board.user_interation()
board.show_grid()

