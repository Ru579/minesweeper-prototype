from Cell import *
from random import randint


class Board:
    def __init__(self, grid_height=0, grid_width=0, no_of_mines=0):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.no_of_mines = no_of_mines
        self.grid = [[Cell() for _ in range(0, grid_width)] for _ in range(0, grid_height)]
        self.protected_coordinate = []
        self.flag_difference = 0
        self.was_flagged = False
        self.revealed_cells = 0
        self.not_enough_flags = False
        self.game_over = False
        self.zero_coordinates = []

    def place_mines(self, grid_height, grid_width, no_of_mines):
        for i in range(0, no_of_mines):
            while True:
                x = randint(0, (grid_height - 1))
                y = randint(0, (grid_width - 1))
                if self.grid[x][y].value != "*" and [x, y] != self.protected_coordinate:
                    self.grid[x][y].value = "*"
                    break
        self.calculate_numbers(grid_height, grid_width)

    def calculate_numbers(self, grid_height, grid_width, after_barrel_shift = False):
        for i in range(0, grid_height):
            for j in range(0, grid_width):
                if self.grid[i][j].value != "*":
                    #self.grid[i][j].value = self.count_surroundings(i, j, lambda cell: cell.value == "*")
                    if not after_barrel_shift:
                        self.grid[i][j].value = self.count_surroundings(i, j, lambda cell: cell.value == "*", portal_edge=True)
                        if self.grid[i][j].value=="0": #make a function to check all surrounding cells, which also applies to edge cells
                            self.zero_coordinates.append([i,j])
                    else:
                        self.grid[i][j].value = self.count_surroundings(i, j, lambda cell: cell.value == "*")


    def barrel_shift_to_zero_cell(self):
        target_cell = self.zero_coordinates[randint(0,len(self.zero_coordinates)-1)]

        #barrel shifting vertically
        vertical_difference = self.protected_coordinate[0] - target_cell[0]
        if vertical_difference>0:
            for _ in range(vertical_difference):
                self.barrel_shift_down()
        elif vertical_difference<0:
            vertical_difference *= -1
            for _ in range(vertical_difference):
                self.barrel_shift_up()

        #barrel shifting horizontally
        horizontal_difference = self.protected_coordinate[1] - target_cell[1]
        if horizontal_difference>0:
            for _ in range(horizontal_difference):
                self.barrel_shift_right()
        elif horizontal_difference<0:
            horizontal_difference *= -1
            for _ in range(horizontal_difference):
                self.barrel_shift_left()


    def barrel_shift_left(self):
        for row in range(self.grid_height):
            temp_value = self.grid[row][0].value
            del self.grid[row][0]
            self.grid[row].append(Cell(value=temp_value))


    def barrel_shift_right(self):
        for row in range(self.grid_height):
            temp_value = self.grid[row][self.grid_width-1].value
            del self.grid[row][self.grid_width-1]
            self.grid[row].insert(0,Cell(value=temp_value))


    def barrel_shift_up(self):
        temp_row = self.grid[0]
        del self.grid[0]
        self.grid.append(temp_row)


    def barrel_shift_down(self):
        temp_row = self.grid[self.grid_height-1]
        del self.grid[self.grid_height-1]
        self.grid.insert(0,temp_row)


    def calculate_no_of_mines(self, stage, difficulty):
        if difficulty == "Easy":
            return round(0.13 * (stage**2))
            #return round(0.134 * (stage**2))
            #return round(0.12 * (stage ** 2))
            # return round(0.15625 * (stage**2))
        elif difficulty == "Medium":
            return round(0.175 * (stage ** 2))
        elif difficulty == "Hard":
            return round(0.206 * (stage ** 2))
        elif difficulty == "Very Hard":
            return round(0.237 * (stage ** 2))


    def open_cell(self, x, y, game_started):
        if self.grid[x][y].state == "Hidden":
            if not game_started:
                self.protected_coordinate.extend([x, y])
                self.place_mines(self.grid_height, self.grid_width, self.no_of_mines)

                self.barrel_shift_to_zero_cell()
                self.calculate_numbers(self.grid_height, self.grid_width, after_barrel_shift=True)

                #need to recalculate numbers after barrel shifting- pass in "after_barrel_shift = True" so that it won't try to make a list of zero coordinates

            self.grid[x][y].state = "Revealed"
            self.revealed_cells += 1
            if self.grid[x][y].value == "*":
                self.game_over = True
            elif self.grid[x][y].value == "0":
                self.auto_reveal(x, y)

        elif self.grid[x][y].state == "Revealed":
            if self.count_surroundings(x, y, lambda cell: cell.state == "Flagged") == self.grid[x][y].value:
                self.auto_reveal(x, y)
            elif int(self.count_surroundings(x, y, lambda cell: cell.state == "Flagged")) < int(self.grid[x][y].value):
                self.flag_difference = int(self.count_surroundings(x, y, lambda cell: cell.state == "Flagged")) - int(self.grid[x][y].value)
            elif int(self.count_surroundings(x, y, lambda cell: cell.state == "Flagged")) > int(self.grid[x][y].value):
                self.flag_difference = int(self.count_surroundings(x, y, lambda cell: cell.state == "Flagged")) - int(self.grid[x][y].value)

    def flag_cell(self, x, y, mines_left):
        if self.grid[x][y].state != "Revealed":
            if self.grid[x][y].state != "Flagged":
                if mines_left > 0:
                    self.grid[x][y].state = "Flagged"
                else:
                    self.not_enough_flags = True
            elif self.grid[x][y].state == "Flagged":
                self.grid[x][y].state = "Hidden"
                self.was_flagged = True

    def confuse_cell(self, x, y):
        if self.grid[x][y].state != "Revealed":
            if self.grid[x][y].state != "Confused":
                self.grid[x][y].state = "Confused"
            elif self.grid[x][y].state == "Confused":
                self.grid[x][y].state = "Hidden"

    def auto_reveal(self, x, y):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.in_bounds(i, j) and self.grid[i][j].state == "Hidden":
                    self.grid[i][j].state = "Revealed"

                    if self.grid[i][j].value == "*":
                        self.game_over = True

                    self.revealed_cells += 1
                    if self.grid[i][j].value == "0":
                        self.auto_reveal(i, j)

    def reveal_all(self):
        for i in range(0, self.grid_height):
            for j in range(0, self.grid_width):
                self.grid[i][j].state = "Revealed"

    def in_bounds(self, x, y):
        if 0 <= x < self.grid_height and 0 <= y < self.grid_width:
            return True
        else:
            return False

    def get_surrounding_cells(self, x, y):  # returns a list of the coordinates of surrounding cells
        cells = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.in_bounds(i, j):
                    cells.append(self.grid[i][j])
        return cells


    def get_edge_inclusive_surrounding_cells(self,x,y):
        cells=[]
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if self.in_bounds(i,j):
                    cells.append(self.grid[i][j])
                else:
                    if i<0:
                        i=self.grid_height-1
                    elif i>self.grid_height-1:
                        i=0
                    if j<0:
                        j=self.grid_width-1
                    elif j>self.grid_width-1:
                        j=0
                    cells.append(self.grid[i][j])
        return cells


    def count_surroundings(self, x, y, predicate, portal_edge = False):
        count = 0
        if not portal_edge:
            for cell in self.get_surrounding_cells(x, y):
                if predicate(cell):
                    count += 1
        else:
            for cell in self.get_edge_inclusive_surrounding_cells(x,y):
                if predicate(cell):
                    count+=1
        return str(count)




# TO TEST BOARD
# test_grid = [[0 for _ in range(0,8)] for _ in range(0,8)]
# board=Board(8,8,10)
# for i in range(0,8):
#   for j in range(0,8):
#       test_grid[i][j] = board.grid[i][j].value
# print(test_grid)

# FOR TESTING
# test_grid = [[0 for _ in range(0, 8)] for _ in range(0, 8)]
# for i in range(0,8):
#  for j in range(0,8):
#      test_grid[i][j] = self.grid[i][j].value
# print(test_grid)