from tkinter import *


root=Tk()


def switch():
    if b1["state"] == "normal":
        b1["state"] = "disabled"
        b2["text"] = "enable"
    else:
        b1["state"] = "normal"
        b2["text"] = "disable"

#--Buttons
b1 = Button(root, text="Button", height=5, width=7)
b1.grid(row=0, column=0)

b2 = Button(text="disable", command=switch)
b2.grid(row=0, column=1)

mainloop()
