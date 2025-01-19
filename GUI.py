import tkinter as tk
import Game

root = tk.Tk()

tiles=[]


game=Game()

#change 9s for game.grid_size

for i in range(0,9):
    for j in range(0,9):
        tile = tk.Button(root,text=game.grid[i][j],width=2,height=2,command = lambda: print("LEFT CLICK")).grid(row=i,column=j)
        tile.bind("<Button-3>", lambda event: print("RIGHT CLICK"))
        tiles.append(tile)