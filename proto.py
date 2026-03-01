from Cell import Cell
from random import randint

class Board:
    def __init__(self, grid_height, grid_width, no_of_mines):
        #initialising variables
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.no_of_mines = no_of_mines
        self.flags_left = no_of_mines
        self.not_enough_flags = False
        self.game_over = False
        self.protected_coordinate = []
        self.zero_coordinates = []
        
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
    
    def calculate_cell_numbers(self, after_barrel_shift):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.grid[i][j].value != "*":
                    # setting the value of the cell to the number of mines around it
                    self.grid[i][j].value = self.count_surroundings(i, j, lambda cell: cell.value == "*", edge_wrap = not after_barrel_shift)

                    # keeping track of what cells are 0 cells in preparation for barrel shifting
                    if not after_barrel_shift and self.grid[i][j].value == "0":
                        self.zero_coordinates.append([i,j])
    
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

    def barrel_shift_to_zero_cell(self):
        target_cell = self.zero_coordinates[randint(0,len(self.zero_coordinates)-1)]

        #barrel shifting vertically
        vertical_difference = self.protected_coordinate[0] - target_cell[0]
        if vertical_difference>0: # target cell is above where user clicked
            for _ in range(vertical_difference):
                self.barrel_shift_down()
        elif vertical_difference<0: # target cell is below where user clicked
            vertical_difference *= -1
            for _ in range(vertical_difference):
                self.barrel_shift_up()
        
        #barrel shifting horizontally
        horizontal_difference = self.protected_coordinate[1] - target_cell[1]
        if horizontal_difference>0: # target cell is to the left of where user clicked
            for _ in range(horizontal_difference):
                self.barrel_shift_right()
        elif horizontal_difference<0: # target cell is to the right of where user clicked
            horizontal_difference *= -1
            for _ in range(horizontal_difference):
                self.barrel_shift_left()
    
    def barrel_shift_up(self):
        #copying the first row, making it the last row
        temp_row = self.grid[0]
        del self.grid[0]
        self.grid.append(temp_row)
    
    def barrel_shift_down(self):
        #copying the last row, making it the first row
        temp_row = self.grid[self.grid_height-1]
        del self.grid[self.grid_height-1]
        self.grid.insert(0, temp_row)
    
    def barrel_shift_left(self):
        #for each row, copying the first value, removing it, then adding it to the end of the list
        for row in range(self.grid_height):
            temp_value = self.grid[row][0].value
            del self.grid[row][0]
            self.grid[row].append(Cell(value=temp_value))
    
    def barrel_shift_right(self):
        #for each row, copying the last value, removing it, then inserting it at the beginning
        for row in range(self.grid_height-1):
            temp_value = self.grid[row][self.grid_width-1].value
            del self.grid[row][self.grid_width-1]
            self.grid[row].insert(0, Cell(value=temp_value))


        
    def open_cell(self, x, y, game_started):
        if self.grid[x][y].state == "Hidden":
            #creating the board on first left click
            if not game_started:
                self.protected_coordinate.extend([x,y])
                self.place_mines()
                self.calculate_cell_numbers(after_barrel_shift= False)
                self.barrel_shift_to_zero_cell()
                self.calculate_cell_numbers(after_barrel_shift= True)

            
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
        if self.grid[x][y].state != "Revealed":
            if self.grid[x][y].state != "Flagged": # Cell is Hidden or Confused
                # flagging the cell if there are enough flags left
                if self.flags_left > 0:
                    self.grid[x][y].state = "Flagged"
                else:
                    self.not_enough_flags = True
            else: # Cell is flagged
                self.grid[x][y].state = "Hidden"
        

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
            else:
                self.grid[x][y].state = "Hidden"


    def show_grid(self):
        #reading values and states from cell objects
        #self.text_grid_values = [[self.grid[i][j].value for j in range(self.grid_width)] for i in range(self.grid_height)]
        #
        #self.text_grid_states = [[self.grid[i][j].state for j in range(self.grid_width)] for i in range(self.grid_height)]
        #
        #for row in range(self.grid_height):
        #    print(self.text_grid_values[row])
        #for row in range(self.grid_height):
        #    print(self.text_grid_states[row])

        for row in range(self.grid_height):
            current_row = ""
            for column in range(self.grid_width):
                if self.grid[row][column].state == "Hidden":
                    current_row += f"\033[89m X \033[0m"
                elif self.grid[row][column].state == "Revealed":
                    current_row += f"\033[94m {self.grid[row][column].value} \033[0m"
            print(current_row)

    
    def user_interation(self):
        player_active = True
        while player_active:
            game_action = int(input("(1): Open Cell\n(2): Flag Cell\n(3): Confuse Cell\n(4): End Interaction"))
            if game_action != 4:
                x_coordinate = int(input("Enter x coordinate:"))
                y_coordinate = int(input("Enter y coordinate:"))
            if game_action == 1:
                self.open_cell(x_coordinate, y_coordinate, game_started= False)
                if self.game_over:
                    print("GAME OVER")
            elif game_action == 2:
                self.flag_cell(x_coordinate, y_coordinate)
            elif game_action == 3:
                self.confuse_cell(x_coordinate, y_coordinate)
            elif game_action == 4:
                player_active = False


#main code
board = Board(10,10, 8)
board.show_grid()
board.user_interation()
board.show_grid()

