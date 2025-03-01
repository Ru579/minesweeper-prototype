from tkinter import *
from PIL import Image, ImageTk

root = Tk()

#def switch():
#    global state
#    if state:
#        button.config(image=tk_off)
#        state = False
#    elif not state:
#        button.config(image=tk_on)
#        state = True
#    else:
#        print("Didn't work")
#
#
#on = Image.open('on_switch.png')
#on = on.resize((1000, 1000))
#tk_on = ImageTk.PhotoImage(on)
#off = Image.open("off_switch.png")
#off=off.resize((200,200))
#tk_off = ImageTk.PhotoImage(off)
#
#state=True
#
## Create a label and add the image to it
#button=Button(root, image=tk_on, command=lambda: switch())
#button.pack()
#
## Run the window's main loop

img = Image.open("mine_cell_red.png")
img = img.resize((100,100))
img = ImageTk.PhotoImage(img)

Label(root, image=img).pack()

root.mainloop()