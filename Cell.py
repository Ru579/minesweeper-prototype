#from tkinter import *
#from Game import Game
#
#root = Tk()
#
#game = Game()
#
#cells = tiles = [["" for _ in range(0, game.grid_size)] for _ in range(0, game.grid_size)]
#
#
#def open_cell(tile, x, y):
#    tile.config(state=DISABLED, text=game.grid[x][y])
#    if game.grid[x][y] == "*":
#        print("GAME OVER!")
#        tile.config(bg="red")
#    else:
#        tile.config(bg="white")
#
#
#def flag_cell(tile, x, y):
#    if tile["state"] != DISABLED and (cells[x][y]).state != "Flagged":
#        print(f"Tile ({x},{y}) flagged")
#        tile.config(bg="blue", text="")
#        (cells[x][y]).state = "Flagged"
#    else:
#        print(f"Tile ({x},{y}) unflagged")
#        tile.config(bg="#f0f0f0")
#        (cells[x][y]).state = "Hidden"
#
#
#def confuse_cell(tile, x, y):
#    if tile["state"] != DISABLED and (cells[x][y]).state != "Confused":
#        print(f"Tile ({x},{y}) marked as a question")
#        tile.config(bg="green", text="?")
#        (cells[x][y]).state = "Confused"
#    else:
#        print(f"Tile ({x},{y}) no longer confused")
#        tile.config(bg="#f0f0f0", text="")
#        (cells[x][y]).state = "Hidden"
#
#
#class Cell:
#
#    def __init__(self, row, column):
#        tile = Button(root, text="", width=4, height=2)
#        tile.bind("<Button-1>", lambda event, current_tile=tile, a=row, b=column: open_cell(current_tile, a, b))
#        tile.bind("<Button-2>", lambda event, current_tile=tile, a=row, b=column: confuse_cell(current_tile, a, b))
#        tile.bind("<Button-3>", lambda event, current_tile=tile, a=row, b=column: flag_cell(current_tile, a, b))
#        tile.grid(row=row, column=column)
#        self.button = tile
#        self.state = "Hidden"

