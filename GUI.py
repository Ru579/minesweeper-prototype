from tkinter import *
from Board import *
import time


class Cell:
    def __init__(self, row, column, board):
        tile = Button(root, text="", width=4, height=2, bg="#d8d8d8")
        current_tile=tile
        tile.config(command=lambda a=row, b=column: open_cell(current_tile, a, b, board))
        tile.bind("<Button-2>", lambda event, current_tile=tile, a=row, b=column: confuse_cell(current_tile, a, b))
        tile.bind("<Button-3>", lambda event, current_tile=tile, a=row, b=column: flag_cell(current_tile, a, b))
        tile.grid(row=row, column=column)
        self.button = tile
        self.state = "Hidden"


# Functions for cell buttons

def open_cell(tile, x, y, board):

    #if user clicks on Hidden tile
    if (cells[x][y]).state=="Hidden":
        print(f"Cell ({x},{y}) is {(cells[x][y]).state}")
        if not board.game_started:
            board.game_started = True
            protected_coordinate.extend([x,y])
            board.place_mines(board.grid_size,board.no_of_mines)
        tile.config(text=board.grid[x][y])
        (cells[x][y]).state = "Revealed"
        tile.config(bg="white")
        if board.grid[x][y] == "*":
            print("GAME OVER!")
            tile.config(bg="red")
        elif board.grid[x][y]==0:
            auto_reveal(x,y)

    #if user clicks on revealed number
    if (cells[x][y]).state=="Revealed" and board.grid[x][y]!="*":
        print(f"Cell ({x},{y}) is {(cells[x][y]).state}")
        if number_of_flags(x,y)<(board.grid[x][y]):
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if board.in_bounds(i,j) and (cells[i][j]).state=="Hidden":
                        (cells[i][j]).button.config(bg="white")
                        ((cells[i][j]).button).after(500, lambda row=i,column=j: ((cells[row][column]).button).config(bg="#d8d8d8"))

        #if number_of_flags(x,y)==(board.grid[x][y]):
        #    zero_auto_reveal(x,y)

        if number_of_flags(x,y)>(board.grid[x][y]):
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if board.in_bounds(i,j) and (cells[i][j]).state=="Flagged":
                        (cells[i][j]).button.config(bg="white")
                        ((cells[i][j]).button).after(500, lambda row=i,column=j: ((cells[row][column]).button).config(bg="blue"))


def flag_cell(tile, x, y):
    #tile["state"] != DISABLED and
    state = (cells[x][y]).state
    print(state)
    if state=="Hidden" or state=="Confused":
        print(f"Tile ({x},{y}) flagged")
        tile.config(bg="blue", text="")
        (cells[x][y]).state = "Flagged"
    elif state=="Flagged":
        print(f"Tile ({x},{y}) unflagged")
        tile.config(bg="#d8d8d8")
        (cells[x][y]).state = "Hidden"


def confuse_cell(tile, x, y):
    state = (cells[x][y]).state
    print(state)
    if state == "Hidden" or state == "Flagged":
        print(f"Tile ({x},{y}) marked as a question")
        tile.config(bg="green", text="?")
        (cells[x][y]).state = "Confused"
    elif state == "Confused":
        print(f"Tile ({x},{y}) no longer confused")
        tile.config(bg="#d8d8d8", text="")
        (cells[x][y]).state = "Hidden"


def reveal_all(board):
    for i in range(0,board.grid_size):
        for j in range(0,board.grid_size):
            (cells[i][j]).button.invoke()

def auto_reveal(x,y):
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if board.in_bounds(i,j):
                ((cells[i][j]).button).invoke()

def number_of_flags(x,y):
    flagCount=0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if board.in_bounds(i,j):
                if (cells[i][j]).state == "Flagged": #try to put both if statements in one line
                    flagCount+=1
    return flagCount


# Main Program

root = Tk()

board = Board(10,20)


cells = [["" for _ in range(0, board.grid_size)] for _ in range(0, board.grid_size)]

for i in range(0, board.grid_size):
    for j in range(0, board.grid_size):
        my_cell = Cell(i, j, board)
        cells[i][j] = my_cell

#if input("Enter Password (it's password):")=="password":
#    ultrabutton = Button(root, text="ULT", bg="yellow",width=4, height=2, command = lambda: reveal_all(board)).grid(row=(board.grid_size), column=(board.grid_size))



mainloop()



#### KEY NOTE FOR LATER GUI DESIGN --- columnspan keyword
#title = Label(root,text="MINESWEEPER", padx=20)
#title.grid(row=0,column=(board.grid_size//2),columnspan=(game.grid_size))
##########