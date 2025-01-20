from tkinter import *
from Game import *



class Cell:
    def __init__(self, row, column, game):
        tile = Button(root, text="", width=4, height=2)
        current_tile=tile
        tile.config(command=lambda a=row, b=column: open_cell(current_tile, a, b, game))
        #tile.bind("<Button-1>", lambda event, current_tile=tile, a=row, b=column: open_cell(current_tile, a, b))
        tile.bind("<Button-2>", lambda event, current_tile=tile, a=row, b=column: confuse_cell(current_tile, a, b))
        tile.bind("<Button-3>", lambda event, current_tile=tile, a=row, b=column: flag_cell(current_tile, a, b))
        tile.grid(row=row, column=column)
        self.button = tile
        self.state = "Hidden"


# Functions for cell buttons

def open_cell(tile, x, y, game):
    if (cells[x][y]).state=="Hidden":
        if not game.game_started:
            game.game_started = True
            protected_coordinate.extend([x,y])
            game.place_mines(game.grid_size,game.no_of_mines)
        tile.config(state=DISABLED, text=game.grid[x][y])
        (cells[x][y]).state = "Revealed"
        if game.grid[x][y] == "*":
            print("GAME OVER!")
            tile.config(bg="red")
        else:
            tile.config(bg="white")


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


def reveal_all(game):
    for i in range(0,game.grid_size):
        for j in range(0,game.grid_size):
            (cells[i][j]).button.invoke()


# Main Program

root = Tk()

game = Game()


cells = [["" for _ in range(0, game.grid_size)] for _ in range(0, game.grid_size)]

for i in range(0, game.grid_size):
    for j in range(0, game.grid_size):
        my_cell = Cell(i, j, game)
        cells[i][j] = my_cell

ultrabutton = Button(root, text="ULT", bg="yellow",width=4, height=2, command = lambda: reveal_all(game)).grid(row=(game.grid_size), column=(game.grid_size))



mainloop()



#### KEY NOTE FOR LATER GUI DESIGN --- columnspan keyword
#title = Label(root,text="MINESWEEPER", padx=20)
#title.grid(row=0,column=(game.grid_size//2),columnspan=(game.grid_size))
##########