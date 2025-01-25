from Cell import *
from random import randint


class Board:
    def __init__(self, grid_height=0, grid_width=0, no_of_mines=0):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.no_of_mines = no_of_mines
        self.grid = [[Cell() for _ in range(0, grid_width)] for _ in range(0, grid_height)]
        self.protected_coordinate = []
        self.flag_difference=0

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
                    self.grid[i][j].value = self.count_surroundings(i, j, lambda cell: cell.value == "*")

    def open_cell(self, x, y, game_started):
        if self.grid[x][y].state == "Hidden":
            if not game_started:
                self.protected_coordinate.extend([x, y])
                self.place_mines(self.grid_height, self.grid_width, self.no_of_mines)
            self.grid[x][y].state = "Revealed"
            if self.grid[x][y].value == "*":
                print("GAME OVER!")  # to be replaced with proper game over function
            elif self.grid[x][y].value == "0":
                self.auto_reveal(x, y)

        elif self.grid[x][y].state == "Revealed":
            if self.count_surroundings(x, y, lambda cell: cell.state == "Flagged") == self.grid[x][y].value:
                self.auto_reveal(x, y)
            #Once proper game over feature is added, first part of following if statement can be removed since it won't be possible to click on a revealed mine.
            elif self.grid[x][y].value!="*" and int(self.count_surroundings(x, y, lambda cell: cell.state == "Flagged")) < int(self.grid[x][y].value):
                self.flag_difference = int(self.count_surroundings(x, y, lambda cell: cell.state == "Flagged")) - int(self.grid[x][y].value)
            #Once proper game over feature is added, first part of following if statement can be removed since it won't be possible to click on a revealed mine.
            elif self.grid[x][y].value!="*" and int(self.count_surroundings(x, y, lambda cell: cell.state == "Flagged")) > int(self.grid[x][y].value):
                self.flag_difference = int(self.count_surroundings(x, y, lambda cell: cell.state == "Flagged")) - int(self.grid[x][y].value)

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

    def count_surroundings(self, x, y, predicate):
        count = 0
        for cell in self.get_surrounding_cells(x, y):
            if predicate(cell):
                count += 1
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
