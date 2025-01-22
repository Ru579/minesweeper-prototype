from random import randint

protected_coordinate=[]


class Board:
    def __init__(self, grid_size=8, no_of_mines=20):
        self.grid_size = grid_size
        self.no_of_mines = no_of_mines
        self.game_started = False
        self.grid = [[0 for _ in range(0, grid_size)] for _ in range(0, grid_size)]
        print(self.grid) #CHECKING LINE
        #self.place_mines(grid_size, no_of_mines)

    def place_mines(self, grid_size, no_of_mines):
        for i in range(0, no_of_mines):
            while True:
                x = randint(0, (grid_size - 1))
                y = randint(0, (grid_size - 1))
                if self.grid[x][y]!="*" and [x,y]!=protected_coordinate:
                    self.grid[x][y] = "*"
                    break
        print(self.grid)  # CHECKING LINE
        self.calculate_numbers(grid_size)
        print(self.grid)  # CHECKING LINE

        # make sure mines aren't placed in the same place, also while we're at it make sure that first click isn't a mine (that cell is protected)


    def calculate_numbers(self, grid_size):
        for i in range(0, grid_size):
            for j in range(0, grid_size):
                if self.grid[i][j] != "*":
                    self.grid[i][j] = self.mine_counter(i, j)

    def mine_counter(self, x, y):
        count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.has_mine(i, j):
                    count += 1
        return count

    def has_mine(self, row, column):
        if 0 <= row < self.grid_size and 0 <= column < self.grid_size and self.grid[row][column] == "*":
            return True
        else:
            return False

    def in_bounds(self,x,y):
        if 0<=x<self.grid_size and 0<=y<self.grid_size:
            return True
        else:
            return False



# if row<0 or row>self.grid_size-1 or column<0 or column>self.grid_size-1:
#    return False
# else:
#    if self.grid[row][column]=="*":
#        return Tru
# if row<0 or row>self.grid_size-1:
#    return False
# else:
#    if column<0 or column>self.grid_size-1:
#        return False
#    else:
#        if self.grid[row][column]=="*":
#            return True

# old code for mine_counter
# for i in range(x-1 if x>0 else x, x+2 if x<self.grid_size-1 else x+1):
# for j in range(y-1 if y>0 else y, y+2 if y<self.grid_size-1 else y+1):
# if self.grid[i][j]=="*":
