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
        self.flag_difference = 0
        
        self.game_over = False

        self.protected_coordinate = []
        self.zero_coordinates = []

        #settings
        self.chording_enabled = True
        
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
        #revealing a hidden cell
        if self.grid[x][y].state == "Hidden":
            #creating the board on first left click
            if not game_started:
                self.protected_coordinate.extend([x,y])
                self.place_mines()
                self.calculate_cell_numbers(after_barrel_shift= False)
                self.barrel_shift_to_zero_cell()
                # recalculating the non-edge-wrapped numbers on cells for the user
                self.calculate_cell_numbers(after_barrel_shift= True)

            
            self.grid[x][y].state = "Revealed"

            if self.grid[x][y].value == "*":
                self.game_over = True
            elif self.grid[x][y].value == "0":
                self.auto_reveal_surroundings(x, y)
        
        # chording
        elif self.chording_enabled and self.grid[x][y].state == "Revealed":
            surrounding_flags = self.count_surroundings(x, y, lambda cell: cell.state == "Flagged", edge_wrap= False)
            # successful chording
            if surrounding_flags == self.grid[x][y].value:
                self.auto_reveal_surroundings(x, y)
            # unsuccessful chording
            else:
                self.flag_difference = int(surrounding_flags) - int(self.grid[x][y].value)
                # flag difference is positive if too many flags, negative if too few flags
    
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
                    self.flags_left -= 1
                else:
                    self.not_enough_flags = True
            else: # Cell is already flagged
                self.grid[x][y].state = "Hidden"
                self.flags_left += 1
        
    
    def confuse_cell(self, x, y):
        state = self.grid[x][y].state
        if state != "Revealed":
            if state == "Confused":
                self.grid[x][y].state = "Hidden"
            else: # Cell is flagged or hidden
                if state == "Flagged":
                    self.flags_left += 1
                self.grid[x][y].state = "Confused"

        #if self.grid[x][y].state != "Revealed":
        #    if self.grid[x][y].state != "Confused": 
        #        self.grid[x][y].state = "Confused"
        #    else:
        #        self.grid[x][y].state = "Hidden"


    def show_grid(self):
        for row in range(self.grid_height):
            current_row = ""
            for column in range(self.grid_width):
                state = self.grid[row][column].state
                #representing hidden cells with black 'X's
                if state == "Hidden":
                    current_row += f"\033[30m X \033[0m"
                #representing revealed cells with their value in blue
                elif state == "Revealed":
                    current_row += f"\033[94m {self.grid[row][column].value} \033[0m"
                # representing flagged cells with their value in dark red
                elif state == "Flagged":
                    current_row += f"\033[31m F \033[0m"
                #representing confused cells with their value in dark green
                elif state == "Confused":
                    current_row += f"\033[32m C \033[0m"
            print(current_row)

    
    def user_interation(self):
        player_active = True
        while player_active:
            game_action = int(input("(1): Open Cell\n(2): Flag Cell\n(3): Confuse Cell\n(4): Show grid\n(5): End Interaction\n"))
            if game_action != 5 and game_action != 4:
                x_coordinate = int(input("Enter x coordinate:"))
                y_coordinate = int(input("Enter y coordinate:"))
            if game_action == 1:
                self.open_cell(x_coordinate, y_coordinate, game_started= False)
                if self.game_over:
                    print("GAME OVER")
            elif game_action == 2:
                self.flag_cell(x_coordinate, y_coordinate)
                print(f"Cell as {x_coordinate}, {y_coordinate} is now {self.grid[x_coordinate][y_coordinate].state}")
            elif game_action == 3:
                self.confuse_cell(x_coordinate, y_coordinate)
            elif game_action == 4:
                self.show_grid()
            elif game_action == 5:
                player_active = False


#main code
board = Board(10,10, 8)
board.show_grid()
board.user_interation()
board.show_grid()

#values = [1, 2, 3, 4, 5]
#values.insert(5, 6)
#print(values)

# CHANGE barrel shifting left/right into one function in a future iteration since the code is quite repetitive

