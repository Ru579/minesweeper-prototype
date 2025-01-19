from tkinter import *
from Game import Game

root = Tk()

tiles=[]


game=Game()

#change 9s for game.grid_size

for i in range(0,game.grid_size):
    for j in range(0,game.grid_size):
        tile = Button(root,text=game.grid[i][j],width=2,height=2,command = lambda: print("LEFT CLICK"))
        tile.bind("<Button-3>", lambda event: print("RIGHT CLICK"))
        tile.grid(row=i,column=j)
        tiles.append(tile)


mainloop()