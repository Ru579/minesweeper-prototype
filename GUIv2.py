from GameManager import *
from tkinter import *


def ui_open_cell(x,y):
    game.open_cell(x,y)
    if game.multi_revealed_occurred:
        update_ui()
    else:
        tiles[x][y].config(text=game.get_cell(x,y,"value"))


def ui_flag_cell(x,y):
    game.board.flag_cell(x,y)
    if game.get_cell(x,y,"state")=="Flagged":
        tiles[x][y].config(bg="blue")
    if game.get_cell(x,y,"state")=="Hidden":
        tiles[x][y].config(bg="#d8d8d8")


def ui_confuse_cell(x,y):
    game.board.confuse_cell(x, y)
    if game.get_cell(x, y, "state") == "Confused":
        tiles[x][y].config(bg="green")
    if game.get_cell(x, y, "state") == "Hidden":
        tiles[x][y].config(bg="#d8d8d8")


def update_ui():
    for i in range(0,game.board.grid_height):
        for j in range(0, game.board.grid_width):
            if game.get_cell(i,j,"state")=="Revealed":
                tiles[i][j].config(text=game.get_cell(i,j,"value"))






game = GameManager()

classic_win = Tk()

game.start_classic_mode("Beginner")

tiles = [[Button(classic_win) for _ in range(0,game.board.grid_width)] for _ in range(0,game.board.grid_height)]

for i in range(0, game.board.grid_height):
    for j in range(0, game.board.grid_width):
        tile = Button(classic_win, text="", width=4, height=2, bg="#d8d8d8")
        current_tile = tile
        tile.config(command = lambda row=i, column=j: ui_open_cell(row,column))
        tile.bind("<Button-2>", lambda event, row=i, column=j: ui_confuse_cell(row, column))
        tile.bind("<Button-3>", lambda event, row=i, column=j: ui_flag_cell(row, column))
        tile.grid(row=i, column=j)
        tiles[i][j] = tile


mainloop()
