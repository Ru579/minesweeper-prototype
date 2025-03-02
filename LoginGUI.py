from DatabaseHandler import *
from tkinter import *
from PIL import Image, ImageTk

sign_in_window = Label(None)


def log_in(main_menu, log_in_button):
    log_in_options = Menu(main_menu, tearoff=False)
    if log_in_button.cget("text") != "Not Signed In":
        log_in_options.add_command(label="Sign Out", command=lambda: sign_out())
        log_in_options.add_command(label="Sign in with a different user", command=lambda: different_user_log_in())
    else:
        log_in_options.add_command(label="Sign In", command=lambda: sign_in(main_menu))
    try:
        x = log_in_button.winfo_rootx()
        y = log_in_button.winfo_rooty()
        log_in_options.tk_popup(x, y)
    finally:
        log_in_options.grab_release()


def sign_in(main_menu):
    global sign_in_window
    sign_in_window = Toplevel(main_menu)
    sign_in_window.title("Sign In")
    sign_in_window.geometry("600x400")

    # creating logo
    # logo = Image.open("mine_cell_red.png")
    ##logo = logo.resize((500,500))
    # logo = ImageTk.PhotoImage(logo)
    # logo_label = Label(sign_in_window, image=logo, width=150, height=150)
    ##logo_label = Label(sign_in_window, text="HELLO")
    # print("logo placed")
    ##logo_label.place(x=10, y=0)
    # logo_label.pack()
    logo_label = Label(sign_in_window, image=logo, width=150, height=150)
    logo_label.place(x=10, y=110)

    Label(sign_in_window, text="Sign into Minesweeper", font=("Calibri", 16)).place(x=10, y=10)

    username_sign_in(sign_in_window)


def username_sign_in(window):
    # creating username_sign_in_frame
    username_sign_in_frame = Frame(window, width=450, height=350)
    username_sign_in_frame.place(x=175, y=50)

    Label(username_sign_in_frame, text="Username:", font=("Calibri", 14)).place(x=15, y=130)
    username_entry = Entry(username_sign_in_frame, font=("Calibri", 14), width=25)
    username_entry.place(x=120, y=130)

    warning_text = Label(username_sign_in_frame, text="", font=("Calibri", 11), fg="red")
    warning_text.place(x=260, y=190)

    Button(username_sign_in_frame, text="Create Account?", font=("Calibri", 13), command=lambda: create_account()).place(x=180, y=310)
    Button(username_sign_in_frame, text="Continue", font=("Calibri Bold", 13), bg="blue", command=lambda: confirm_username(username_entry.get(), warning_text, username_sign_in_frame)).place(x=330, y=310)


def password_sign_in(username, username_frame):
    #switching username with password sign in frame
    username_frame.forget()
    password_sign_in_frame = Frame(sign_in_window, width=450, height=350)
    password_sign_in_frame.place(x=175, y=50)

    Label(password_sign_in_frame, text=f"Username: {username}", font=("Calibri", 12)).place(x=15, y=130)
    Label(password_sign_in_frame, text="Password:", font=("Calibri", 14)).place(x=25, y=145)
    password_entry = Entry(password_sign_in_frame, font=("Calibri", 14), width=25)
    password_entry.place(x=130,y=145)

    pword_warning_text = Label(password_sign_in_frame, text="", font=("Calibri", 11), fg="red")
    pword_warning_text.place(x=260, y=190)

    #need to add a confirm button with a different command that checks to see if the entered password is equal to the top line of the located file (top line of any file will be the password assigned to that user)
    #confirm button also needs an alternative else to config the pword_warning_text

    #add a back button to destroy this frame and replace it with the username_sign_in_frame, whose entry's text will then be defaulted to the previously entered username

    #see if you can get characters in the entry to appear as dots like a normal password- possibly add an eye image to toggle reveal these dots
    #add an in game note specifying whether the username and password are case sensitive





def create_account():
    pass


def confirm_username(entry, warning_text, username_frame):
    username_found = database.find_user_file(entry)
    if not username_found:
        warning_text.config(text="Username not found")
    else:
        password_sign_in(entry, username_frame)


def sign_out():
    pass


def different_user_log_in():
    pass


database = DatabaseHandler()

main_menu = Tk()
log_in_button = Button(main_menu, text="Not Signed In", command=lambda: log_in(main_menu, log_in_button))
log_in_button.pack()

logo = Image.open("mine_cell_red.png")
logo = logo.resize((150, 150))
logo = ImageTk.PhotoImage(logo)
# logo_label = Label(main_menu, image=logo, width=150, height=150)


mainloop()
