from LoginGUI import *
from DatabaseHandler import DatabaseHandler

root = Tk()

database = DatabaseHandler()
Label(root, text="TITLE HERE", font=("Calibri Bold", 30)).grid(row=0, column=1)
Label(root, text="SETTINGS").grid(row=0, column=0)
Label(root, text="BUTTONS", width=20, font=("Calibri", 15)).grid(row=1, column=1)
loginGUI = LoginGUI(database)
loginGUI.create_profile(root)

mainloop()


