from tkinter import *
from Game import *



class Cell:
    def __init__(self, row, column, input_game_started):
        tile = Button(root, text="", width=4, height=2)
        current_tile=tile
        tile.config(command=lambda a=row, b=column: open_cell(current_tile, a, b, input_game_started))
        #tile.bind("<Button-1>", lambda event, current_tile=tile, a=row, b=column: open_cell(current_tile, a, b))
        tile.bind("<Button-2>", lambda event, current_tile=tile, a=row, b=column: confuse_cell(current_tile, a, b))
        tile.bind("<Button-3>", lambda event, current_tile=tile, a=row, b=column: flag_cell(current_tile, a, b))
        tile.grid(row=row, column=column)
        self.button = tile
        self.state = "Hidden"


# Functions for cell buttons

def open_cell(tile, x, y, input_game_started):
    #if not input_game_started:
    #    global game_started
    #    game_started=True
    #    protected_coordinate.extend([x,y])
    #    game.place_mines(game.grid_size,game.no_of_mines)
    tile.config(state=DISABLED, text=game.grid[x][y])
    if game.grid[x][y] == "*":
        print("GAME OVER!")
        tile.config(bg="red")
    else:
        tile.config(bg="white")

    #if (input("s to show all mines")=="s"):
    #    for i in range(0,game.grid_size):
    #        for j in range(0,game.grid_size):
    #            (cells[i][j]).button.invoke()


def flag_cell(tile, x, y):
    if tile["state"] != DISABLED and (cells[x][y]).state != "Flagged":
        print(f"Tile ({x},{y}) flagged")
        tile.config(bg="blue", text="")
        (cells[x][y]).state = "Flagged"
    else:
        print(f"Tile ({x},{y}) unflagged")
        tile.config(bg="#f0f0f0")
        (cells[x][y]).state = "Hidden"


def confuse_cell(tile, x, y):
    if tile["state"] != DISABLED and (cells[x][y]).state != "Confused":
        print(f"Tile ({x},{y}) marked as a question")
        tile.config(bg="green", text="?")
        (cells[x][y]).state = "Confused"
    else:
        print(f"Tile ({x},{y}) no longer confused")
        tile.config(bg="#f0f0f0", text="")
        (cells[x][y]).state = "Hidden"


# Main Program

root = Tk()

game = Game()
game_started = False


cells = [["" for _ in range(0, game.grid_size)] for _ in range(0, game.grid_size)]

for i in range(0, game.grid_size):
    for j in range(0, game.grid_size):
        my_cell = Cell(i, j, game_started)
        cells[i][j] = my_cell


mainloop()



#### KEY NOTE FOR LATER GUI DESIGN --- columnspan keyword
#title = Label(root,text="MINESWEEPER", padx=20)
#title.grid(row=0,column=(game.grid_size//2),columnspan=(game.grid_size))
##########