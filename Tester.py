## Import the required libraries
#from tkinter import *
#from tkinter import messagebox
#
## Create an instance of tkinter frame
#root = Tk()
#
## Set the size of the tkinter window
#root.geometry("700x350")
#
#def display_msg():
#   messagebox.showinfo("Message", "Hello There! Greeting from TutorialsPoint.")
#
## Add a Button widget
#b1 = Button(root, text="Click Me", command=display_msg)
#b1.bind("<Button-3>", lambda event: print("HELLO"))
#b1.pack(pady=30)
#b1.invoke()
#
#root.mainloop()

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
        if number_of_flags(x,y)<(board.grid[x][y]):
            #brighten the surrounding hidden squares
            pass
        if number_of_flags(x,y)==(board.grid[x][y]):
            auto_reveal(x,y)
        if number_of_flags(x,y)>(board.grid[x][y]):
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if board.in_bounds(x,y) and (cells[i][j]).state=="Flagged":
                        (cells[i][j]).button.config(bg="white")
                        ((cells[i][j]).button).after(1000,lambda: ((cells[i][j]).button).config(bg="#d8d8d8"))





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
        tile.config(bg="#f0f0f0")
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
        tile.config(bg="#f0f0f0", text="")
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
                if (cells[i][j]).state == "Flagged": ##try to put both if statements in one line
                    flagCount+=1
    return flagCount
