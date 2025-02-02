from tkinter import *

test = Tk()

frame = Frame(test, width=1000, height=1000)
frame.bind("<Button-1>", lambda event: print("left clicked"))
frame.pack()

mainloop()