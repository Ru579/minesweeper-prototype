from tkinter import *
from Game import Game

root = Tk()

#tiles=[]


def open_cell(tile,x,y):
    tile.config(state = DISABLED)
    if game.grid[x][y]=="*":
        print("GAME OVER!")

def flag_cell(tile,x,y):
    if tile["state"]!=DISABLED:
        print(f"Tile ({x},{y}) flagged")
        tile.config(bg="blue")




game=Game()


tiles=[["BLANK" for _ in range(0,game.grid_size)] for _ in range(0,game.grid_size)]

for i in range(0,game.grid_size):
    for j in range(0,game.grid_size):
        tile = Button(root,text=game.grid[i][j],width=4,height=2,command = lambda: print("LEFT CLICK"))

        #to be removed: sets colour of mines to red
        if game.grid[i][j]=="*":
            tile.config(bg="red")
        #####

        tile.bind("<Button-1>", lambda event, current_tile=tile, a=i, b=j: open_cell(current_tile,a,b))
        tile.bind("<Button-3>", lambda event, current_tile=tile, a=i, b=j: flag_cell(current_tile,a,b))
        tile.grid(row=i,column=j)

        tiles[i][j]=tile #UNCERTAIN CODE
        #tiles.append(tile)


mainloop()