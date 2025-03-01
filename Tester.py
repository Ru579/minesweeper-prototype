from tkinter import *
from PIL import Image, ImageTk

root = Tk()

img = Image.open("mine_cell_red.png")
img = img.resize((100,100))
img = ImageTk.PhotoImage(img)

label = Label(root, image=img)
label.pack()

print(label.cget("image"))
print(img)
if label.cget("image")==str(img):
    print("It's a mine")
else:
    print("Not a mine?")

root.mainloop()