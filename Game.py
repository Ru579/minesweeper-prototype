from random import randint

class Game:
    def __init__(self, grid_size=8, no_of_mines=20):
        self.grid_size=grid_size
        self.grid=[[0 for i in range(0,grid_size)] for j in range(0,grid_size)]
        print(self.grid)
        self.place_mines(grid_size, no_of_mines)


    def place_mines(self, grid_size, no_of_mines):
        for i in range(0,no_of_mines):
            x = randint(0,(grid_size-1))
            y = randint(0,(grid_size-1))
            self.grid[x][y] = "*"
        print(self.grid)

        #REMOVE THIS LATER

        self.calculate_numbers(grid_size)
        print(self.grid)


    def calculate_numbers(self, grid_size):
        for i in range(0,grid_size):
            for j in range(0,grid_size):
                if self.grid[i][j]!="*":
                    self.grid[i][j]=self.mine_counter(i,j)


    def mine_counter(self,x,y):
        count=0
        for i in range(x-1 if x>0 else x, x+2 if x<self.grid_size-1 else x+1):
            for j in range(y-1 if y>0 else y, y+2 if y<self.grid_size-1 else y+1):
                if self.grid[i][j]=="*":
                    count+=1
        return count

    def has_mine(self,x,y):
        #check if out of bounds
        #return false if so
        #if in bounds, check if mine is present
        pass



game = Game()
