from Cell import *
from random import randint


class Board:
    def __init__(self, grid_height=0, grid_width=0, no_of_mines=0):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.no_of_mines = no_of_mines
        self.grid = [[Cell() for _ in range(0, grid_width)] for _ in range(0, grid_height)]
        self.protected_coordinate = []
        # self.multi_reveal_occurred = False
        self.place_mines(grid_height, grid_width, no_of_mines)  # TO BE REMOVED

    def place_mines(self, grid_height, grid_width, no_of_mines):
        for i in range(0, no_of_mines):
            while True:
                x = randint(0, (grid_height - 1))
                y = randint(0, (grid_width - 1))
                if self.grid[x][y].value != "*" and [x, y] != self.protected_coordinate:
                    self.grid[x][y].value = "*"
                    break
        self.calculate_numbers(grid_height, grid_width)

    def calculate_numbers(self, grid_height, grid_width):
        for i in range(0, grid_height):
            for j in range(0, grid_width):
                if self.grid[i][j].value != "*":
                    self.grid[i][j].value = self.mine_counter(i, j)

    def mine_counter(self, x, y):
        count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.has_mine(i, j):
                    count += 1
        return str(count)

    def has_mine(self, row, column):
        if self.in_bounds(row, column) and self.grid[row][column].value == "*":
            return True
        else:
            return False

    def in_bounds(self, x, y):
        if 0 <= x < self.grid_height and 0 <= y < self.grid_width:
            return True
        else:
            return False

    def open_cell(self, x, y, game_started):
        # self.multi_reveal_occurred = False
        if self.grid[x][y].state == "Hidden":
            if not game_started:
                self.protected_coordinate.extend([x, y])
                self.place_mines(self.grid_height, self.grid_width, self.no_of_mines)
            self.grid[x][y].state = "Revealed"
            if self.grid[x][y].value == "*":
                print("GAME OVER!")  # to be replaced with proper game over function
            elif self.grid[x][y].value == "0":
                self.auto_reveal(x, y)
                # self.multi_reveal_occurred = True

        elif self.grid[x][y].state == "Revealed":
            if self.number_of_flags(x, y) == self.grid[x][y].value:
                self.auto_reveal(x, y)
                # self.multi_reveal_occurred = True

    def flag_cell(self, x, y):
        if self.grid[x][y].state != "Revealed":
            if self.grid[x][y].state != "Flagged":
                self.grid[x][y].state = "Flagged"
                print(f"Tile ({x},{y}) flagged")  # CHECKING LINE
            elif self.grid[x][y].state == "Flagged":
                self.grid[x][y].state = "Hidden"
                print(f"Tile ({x},{y}) unflagged")  # CHECKING LINE

    def confuse_cell(self, x, y):
        if self.grid[x][y].state != "Revealed":
            if self.grid[x][y].state != "Confused":
                self.grid[x][y].state = "Confused"
                print(f"Tile ({x},{y}) marked as a question")  # CHECKING LINE
            elif self.grid[x][y].state == "Confused":
                self.grid[x][y].state = "Hidden"
                print(f"Tile ({x},{y}) no longer marked as a question")  # CHECKING LINE

    def auto_reveal(self, x, y):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.in_bounds(i, j) and self.grid[i][j].state == "Hidden":
                    self.grid[i][j].state = "Revealed"
                    if self.grid[i][j].value == "0":
                        self.auto_reveal(i, j)

    def reveal_all(self):
        for i in range(0, self.grid_height):
            for j in range(0, self.grid_width):
                self.grid[i][j].state = "Revealed"

    def get_surrounding_cells(self,x,y): #returns a list of the coordinates of surrounding cells
        pass

    def count_surroundings(self,x,y,predicate):
        pass
        #takes in a boolean checking funcion, applies it to cell in Cells (gotten from get_surrounding_cells method)


    def number_of_flags(self, x, y):
        flag_count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.in_bounds(i, j) and self.grid[i][j].state=="Flagged":
                    flag_count += 1
        return str(flag_count)

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
