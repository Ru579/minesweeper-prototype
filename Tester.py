from tkinter import *

root = Tk()
root.geometry("1000x1000")


def open_popup():
    mini = Toplevel(root)
    mini.geometry("500x500")
    mini.title("My cool test")
    Label(mini, text="my tester text").place(x=250, y=250)
    Entry(mini).place(x=100,y=100)
    Button(mini, text="CONFIRM", command=mini.destroy).place(x=200,y=400)

Button(root, text="CLICK ME", command= open_popup).pack()

mainloop()

#from tkinter import *
##Create an instance of Tkinter frame
#win = Tk()
##Set the geometry of Tkinter frame
#win.geometry("750x270")
#
#def open_popup():
#   top= Toplevel(win)
#   top.geometry("750x250")
#   top.title("Child Window")
#   Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)
#
#Label(win, text=" Click the Below Button to Open the Popup Window", font=('Helvetica 14 bold')).pack(pady=20)
##Create a button in the main Window to open the popup
#Button(win, text= "Open", command= open_popup).pack()
#win.mainloop()