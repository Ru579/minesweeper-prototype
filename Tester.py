from symbol import pass_stmt
from tkinter import *

root=Tk()

root.after(1000, pass_stmt)
print("Hello")