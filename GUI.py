from tkinter import *
from Game import Game

root = Tk()

#tiles=[]


def open_cell(tile,x,y):
    tile.config(state = DISABLED, text=game.grid[x][y])
    if game.grid[x][y]=="*":
        print("GAME OVER!")
        tile.config(bg = "red")
    else:
        tile.config(bg="white")

def flag_cell(tile,x,y):
    if tile["state"]!=DISABLED and cell_states[x][y]!="Flagged":
        print(f"Tile ({x},{y}) flagged")
        tile.config(bg="blue",text="")
        cell_states[x][y]="Flagged"
    else:
        print(f"Tile ({x},{y}) unflagged")
        tile.config(bg="#f0f0f0")
        cell_states[x][y] = "Unflagged"

def confuse_cell(tile,x,y):
    if tile["state"]!=DISABLED and cell_states[x][y]!="Confused":
        print(f"Tile ({x},{y}) marked as a question")
        tile.config(bg="green", text="?")
        cell_states[x][y]="Confused"
    else:
        print(f"Tile ({x},{y}) no longer confused")
        tile.config(bg="#f0f0f0", text="")
        cell_states[x][y] = "Unflagged"




game=Game(16,50)


tiles=[["BLANK" for _ in range(0,game.grid_size)] for _ in range(0,game.grid_size)]
cell_states=[["Unflagged" for _ in range(0,game.grid_size)] for _ in range(0,game.grid_size)]


for i in range(0,game.grid_size):
    for j in range(0,game.grid_size):
        tile = Button(root,text="",width=4,height=2)

        #to be removed: sets colour of mines to red
        #if game.grid[i][j]=="*":
        #    tile.config(bg="red")
        #####

        tile.bind("<Button-1>", lambda event, current_tile=tile, a=i, b=j: open_cell(current_tile,a,b))
        tile.bind("<Button-2>", lambda event, current_tile=tile, a=i, b=j: confuse_cell(current_tile,a,b))
        tile.bind("<Button-3>", lambda event, current_tile=tile, a=i, b=j: flag_cell(current_tile,a,b))
        tile.grid(row=i,column=j)

        tiles[i][j]=tile #UNCERTAIN CODE
        #tiles.append(tile)


mainloop()