import os

for files in os.listdir("ms_user_data/classic"):
    print(files)

file = open("ms_user_data/settings/test_settings.txt")
data = file.readlines()
print(data[0])

#from DatabaseHandler import *
#from tkinter import *
#from PIL import Image, ImageTk
#
#
#sign_in_window = None
#logo = None
#open_eye = None
#closed_eye = None
#gui_button = None
#menu = None
#profile_pic = None
#
#
#def log_in(main_menu, log_in_button, images):
#    global logo, open_eye, closed_eye, gui_button, menu
#    logo = images[0]
#    open_eye = images[1]
#    closed_eye = images[2]
#    gui_button = log_in_button
#    menu = main_menu
#
#    log_in_options = Menu(main_menu, tearoff=False)
#    if log_in_button.cget("text") != "Log In":
#        log_in_options.add_command(label="Sign Out", command=lambda: sign_out())
#        log_in_options.add_command(label="Sign in with a different user", command=lambda: different_user_log_in())
#    else:
#        log_in_options.add_command(label="Sign In", command=lambda: sign_in(main_menu))
#    try:
#        x = log_in_button.winfo_rootx()
#        y = log_in_button.winfo_rooty()
#        log_in_options.tk_popup(x, y)
#    finally:
#        log_in_options.grab_release()
#
#    #add functionality where, if you successfully sign in, log_in_buttons is .config()-ed to show username
#
#
#def sign_in(main_menu):
#    global sign_in_window
#    sign_in_window = Toplevel(main_menu)
#    sign_in_window.title("Sign In")
#    sign_in_window.geometry("600x400")
#
#    logo_label = Label(sign_in_window, image=logo, width=150, height=150)
#    logo_label.place(x=10, y=110)
#
#    Label(sign_in_window, text="Sign into Minesweeper", font=("Calibri", 16)).place(x=10, y=10)
#
#    username_sign_in(sign_in_window)
#
#
#def username_sign_in(window):
#    # creating username_sign_in_frame
#    username_frame = Frame(window, width=450, height=350)
#    username_frame.place(x=175, y=50)
#
#    Label(username_frame, text="Username:", font=("Calibri", 14)).place(x=15, y=130)
#
#    username_input = StringVar(username_frame)
#    username_entry = Entry(username_frame, font=("Calibri", 14), width=25, textvariable=username_input)
#    username_entry.place(x=120, y=130)
#
#    warning_text = Label(username_frame, text="", font=("Calibri", 11), fg="red")
#    warning_text.place(x=260, y=190)
#
#    Button(username_frame, text="Create Account?", font=("Calibri Bold", 13), fg="#258cdb", command=lambda: create_account()).place(x=180, y=310)
#    Button(username_frame, text="Continue", font=("Calibri Bold", 13), bg="#258cdb", command=lambda: confirm_username(username_input.get(), warning_text, username_frame)).place(x=330, y=310)
#
#
#def confirm_username(username_input, warning_text, username_frame):
#    username_found = database.find_user_file(username_input.lower())
#    if not username_found:
#        warning_text.config(text="Username not found")
#    else:
#        password_sign_in(username_input.lower(), username_frame)
#
#
#def password_sign_in(username, username_frame):
#    # switching username with password sign in frame
#    username_frame.forget()
#    password_frame = Frame(sign_in_window, width=450, height=350)
#    password_frame.place(x=175, y=50)
#
#    Label(password_frame, text=f"Username: {username}", font=("Calibri", 12)).place(x=15, y=130)
#    Label(password_frame, text="Password:", font=("Calibri", 14)).place(x=15, y=160)
#
#    password_input = StringVar(password_frame)
#    password_entry = Entry(password_frame, font=("Calibri", 14), width=25, show="*", textvariable=password_input)
#    password_entry.place(x=120, y=160)
#
#    view_pword_toggle = Button(password_frame, image=open_eye, width=30, height=22,
#                               command=lambda:
#                               switch_eye_image(view_pword_toggle, password_entry, password_input, password_input, password_frame))
#    view_pword_toggle.place(x=380, y=160)
#
#    pword_warning_text = Label(password_frame, text="", font=("Calibri", 11), fg="red")
#    pword_warning_text.place(x=260, y=220)
#
#    Button(password_frame, text="Sign In", font=("Calibri Bold", 13), bg="#258cdb", command=lambda: confirm_password(password_input.get(), pword_warning_text, username)).place(x=330,y=310)
#    Button(password_frame, text="Back", font=("Calibri Bold", 13), fg="#258cdb", command=lambda: back_to_username_frame(username_frame, password_frame)).place(x=180, y=310)
#    # adjust this button's x coordinate placement so that there is a constant distance between the two buttons in the bottom right corner
#
#    Label(password_frame, text="Passwords are case sensitive", font=("Calibri Italic", 10)).place(x=0, y=320)
#    # to be moved?
#
#    # confirm button also needs an alternative else to config the pword_warning_text
#
#
#def confirm_password(password_input, warning_text, username):
#    print(f"user's input is {password_input}")
#    password_correct = database.check_password(password_input)
#    if not password_correct:
#        warning_text.config(text="Incorrect Password")
#    else:#password is correct
#        global profile_pic
#        profile_pic = Canvas(menu, width=60, height=60, bg="#f0f0f0")
#        create_profile_pic(profile_pic, username[0:2].upper())
#        profile_pic.grid(row=0, column=2)
#        gui_button.config(text=username)
#        sign_in_window.destroy()
#
#
#def create_profile_pic(canvas, username_letters):
#    canvas.create_oval(3, 3, 61, 61, fill="green")
#    canvas.create_text(32, 32, text=username_letters, font=("Calibri Bold", 25), anchor="center")
#
#
##READ TO-DO LIST FOR WHAT TO DO WITH CONVERTING THIS FILE INTO A CLASS
#
#
#def back_to_username_frame(username_frame, pword_frame):
#    pword_frame.destroy()
#    username_frame.place(x=175, y=50)
#
#
#def switch_eye_image(button, entry, user_input, string_variable, frame):
#    if button.cget("image") == str(open_eye):
#        button.config(image=closed_eye)
#        current_input = user_input.get()
#        entry.destroy()
#        entry = Entry(frame, font=("Calibri", 14), width=25, textvariable=string_variable)
#        entry.delete(0, len(user_input.get()) + 1)
#        entry.insert(0, current_input)
#        entry.place(x=120, y=160)
#    else:
#        button.config(image=open_eye)
#        current_input = user_input.get()
#        entry.destroy()
#        entry = Entry(frame, font=("Calibri", 14), width=25, show="*", textvariable=string_variable)
#        entry.delete(0, len(user_input.get()) + 1)
#        entry.insert(0, current_input)
#        entry.place(x=120, y=160)
#
#
#def create_account():
#    pass
#
#
#def sign_out():
#    pass
#
#
#def different_user_log_in():
#    pass
#
#
#database = DatabaseHandler()
#
##main_menu = Tk()
#
## following two lines to be moved into GUI
##log_in_button = Button(main_menu, text="Not Signed In", command=lambda: log_in(main_menu, log_in_button))
##log_in_button.pack()
#
##logo = Image.open("mine_cell_red.png")
##logo = logo.resize((150, 150))
##logo = ImageTk.PhotoImage(logo)
### logo_label = Label(main_menu, image=logo, width=150, height=150)
##
##open_eye = Image.open("open_eye.png")
##open_eye = open_eye.resize((30, 22))
##open_eye = ImageTk.PhotoImage(open_eye)
##
##closed_eye = Image.open("closed_eye.png")
##closed_eye = closed_eye.resize((30, 22))
##closed_eye = ImageTk.PhotoImage(closed_eye)
#
##mainloop()






