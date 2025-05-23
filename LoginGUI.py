from tkinter import *
from PIL import Image, ImageTk
from DatabaseHandler import *

class LoginGUI():
    def __init__(self, database, window):
        #self.menu = menu
        self.menu = None
        self.window = window

        logo = Image.open("Images/mine_cell_red.png")
        logo = logo.resize((150, 150))
        self.logo = ImageTk.PhotoImage(logo)

        open_eye = Image.open("Images/open_eye.png")
        open_eye = open_eye.resize((30, 22))
        self.open_eye = ImageTk.PhotoImage(open_eye)

        closed_eye = Image.open("Images/closed_eye.png")
        closed_eye = closed_eye.resize((30, 22))
        self.closed_eye = ImageTk.PhotoImage(closed_eye)

        pic = Image.open("Images/guest_profile.png")
        pic = pic.resize((60, 60))
        self.guest_image = ImageTk.PhotoImage(pic)

        self.database_handler = database

        #frames
        self.sign_in_frame = None #to be replaced with a swappable frame
        self.username_frame = None
        self.pword_frame = None
        self.create_account_frame = None

        #other widgets
        #self.profile_pic = Canvas(self.menu)
        #self.profile_pic.grid(row=0,column=2)
        self.profile_pic = None


        self.profile_circle = None
        self.guest_profile_pic = None
        self.username_entry = None
        self.user_warning_text=None
        self.pword_entry = None
        self.pword_warning_text = None
        self.create_pword_entry = None
        self.confirm_pword_entry = None
        self.create_account_warning={}

        self.warning_given = {}

        #status variables
        self.signed_in = None


    def create_profile(self, menu):
        self.menu = menu
        self.profile_pic = Canvas(self.menu)
        self.profile_pic.grid(row=0, column=2)

        if self.database_handler.username=="":
            self.signed_in = False
            self.create_guest_profile()
        else:
            self.signed_in = True
            self.create_user_profile()


    def create_guest_profile(self):
        if self.profile_pic is not None:
            self.profile_pic.destroy()

        self.guest_profile_pic = Label(self.menu, image=self.guest_image, width=60, height=60)
        self.guest_profile_pic.bind("<Button-1>", lambda event: self.create_sign_in_frame())
        self.guest_profile_pic.grid(row=0, column=2)


    def create_user_profile(self):
        if self.profile_pic is not None:
            self.profile_pic.destroy()

        #creating profile picture
        self.profile_pic = Canvas(self.menu, width=60, height=60, bg="#f0f0f0")
        self.profile_pic.bind("<Button-1>", lambda event: self.show_log_in_options())
        self.profile_pic.bind("<Button-3>", lambda event: self.change_profile_pic())
        self.profile_circle = self.profile_pic.create_oval(3,3,61,61, fill=self.database_handler.settings.profile_pic_colour)
        self.profile_pic.create_text(32, 32, text=self.database_handler.username[0:2], font=("Calibri Bold", 15), anchor="center")
        self.profile_pic.grid(row=0, column=2)


    def show_log_in_options(self):
        log_in_options = Menu(self.menu, tearoff=False)
        log_in_options.add_command(label="Sign Out", command=lambda: self.sign_out())
        log_in_options.add_command(label="Sign in with a different account", command=lambda: self.different_log_in())
        log_in_options.add_command(label="Create an Account", command=lambda: self.create_sign_in_frame("create_account"))
        try:
            x=self.profile_pic.winfo_rootx()
            y=self.profile_pic.winfo_rooty()
            log_in_options.tk_popup(x,y+60)
        finally:
            log_in_options.grab_release()


    def create_sign_in_frame(self, frame_to_create=""):
        self.sign_in_frame = Frame(self.window, width=700, height=440)
        self.menu.forget()
        self.sign_in_frame.pack()

        #self.sign_in_frame.title("Sign In")
        #self.sign_in_frame.geometry("700x400")

        logo_label = Label(self.sign_in_frame, image=self.logo, width=150, height=150)
        logo_label.place(x=10, y=140)

        #close_button
        Button(self.sign_in_frame, text="X", font=("Calibri", 30), fg="red", height=1, command=lambda:self.return_to_menu()).place(x=650, y=0)

        Label(self.sign_in_frame, text="Sign into Minesweeper", font=("Calibri", 16)).place(x=10, y=10)

        self.place_login_frames(frame_to_create)


    def return_to_menu(self):
        self.sign_in_frame.destroy()
        self.menu.pack()


    def place_login_frames(self, frame_to_create="", forget_create_frame = False):
        if frame_to_create=="create_account":
            self.make_create_account_frame()
        else:
            if forget_create_frame:
                self.create_account_frame.destroy()
            self.username_sign_in()


    def username_sign_in(self):
        self.username_frame = Frame(self.sign_in_frame, width=450, height=350)
        self.username_frame.place(x=175, y=90)

        Label(self.username_frame, text="Username:", font=("Calibri", 14)).place(x=15, y=130)
        username_input = StringVar(self.username_frame)
        self.username_entry = Entry(self.username_frame, font=("Calibri", 14), width=25, textvariable=username_input)
        self.username_entry.place(x=120, y=130)

        self.user_warning_text = Label(self.username_frame, text="", font=("Calibri Bold", 11), fg="red")
        self.user_warning_text.place(x=260, y=190)

        Button(self.username_frame, text="Create Account?", font=("Calibri Bold", 13), fg="#258cdb",
               command=lambda: self.make_create_account_frame("username_frame")).place(x=180, y=310)
        Button(self.username_frame, text="Continue", font=("Calibri Bold", 13), bg="#258cdb",
               command=lambda: self.confirm_username(username_input.get())).place(x=330, y=310)


    def confirm_username(self, username_input):
        if username_input.strip()=="":
            self.user_warning_text.config(text="Please Enter a Username")
        elif not self.database_handler.find_user_file(username_input):
            self.user_warning_text.config(text="Username not found")
        else:
            self.pword_sign_in()


    def pword_sign_in(self):
        # switching username with password sign in frame
        self.username_frame.forget()
        self.pword_frame = Frame(self.sign_in_frame, width=450, height=350)
        self.pword_frame.place(x=175, y=90)

        Label(self.pword_frame, text=f"Username: {self.database_handler.temp_username}", font=("Calibri", 12)).place(x=15, y=130)
        Label(self.pword_frame, text="Password:", font=("Calibri", 14)).place(x=15, y=160)

        pword_input = StringVar(self.pword_frame)
        self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
        self.pword_entry.place(x=120, y=160)

        view_pword_toggle = Button(self.pword_frame, image=self.open_eye, width=30, height=22,
                                   command=lambda: self.switch_eye_image(view_pword_toggle, pword_input, "pword"))
        view_pword_toggle.place(x=380, y=160)

        self.pword_warning_text = Label(self.pword_frame, text="", font=("Calibri Bold", 11), fg="red")
        self.pword_warning_text.place(x=260, y=220)

        Button(self.pword_frame, text="Sign In", font=("Calibri Bold", 13), bg="#258cdb",
               command=lambda: self.confirm_pword(pword_input.get())).place(x=330, y=310)
        Button(self.pword_frame, text="Back", font=("Calibri Bold", 13), fg="#258cdb",
               command=lambda: self.back_to_username_frame()).place(x=180, y=310)


    def confirm_pword(self, pword_input):
        pword_correct = self.database_handler.check_pword(pword_input)
        if not pword_correct:
            self.pword_warning_text.config(text="Incorrect Password")
        else:
            self.database_handler.sign_in_user()
            self.create_user_profile()
            self.return_to_menu()


    def back_to_username_frame(self):
        self.pword_frame.destroy()
        self.username_frame.place(x=175,y=90)


    def make_create_account_frame(self, previous_frame=""):
        if previous_frame=="username_frame":
            self.username_frame.forget()

        self.create_account_frame = Frame(self.sign_in_frame, width=550, height=350)
        self.create_account_frame.place(x=175, y=90)

        Label(self.create_account_frame, text="Username:", font=("Calibri", 12)).place(x=50, y=50)
        username_input = StringVar(self.create_account_frame)
        username_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, textvariable=username_input)
        username_entry.place(x=150, y=50)

        Label(self.create_account_frame, text="Password:", font=("Calibri", 12)).place(x=50, y=150)
        pword_input1 = StringVar(self.create_account_frame)
        self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input1)
        self.create_pword_entry.place(x=150, y=150)
        view_create_pword_toggle = Button(self.create_account_frame, image=self.open_eye, width=30, height=22,
                                          command=lambda: self.switch_eye_image(view_create_pword_toggle, pword_input1, "create_pword"))
        view_create_pword_toggle.place(x=360, y=150)

        Label(self.create_account_frame, text="Confirm Password:", font=("Calibri", 12)).place(x=10, y=250)
        pword_input2 = StringVar(self.create_account_frame)
        self.confirm_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input2)
        self.confirm_pword_entry.place(x=150, y=250)

        #self.create_account_pword_warning = Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red")
        #self.create_account_pword_warning.place(x=250, y=270)

        Button(self.create_account_frame, text="Sign In", font=("Calibri Bold", 13), fg="#258cdb", command=lambda: self.place_login_frames("username_frame", True)).place(x=220, y=310)
        Button(self.create_account_frame, text="Create Account", font=("Calibri Bold", 13), bg="#258cdb", command=lambda: self.account_validator(username_input.get(), pword_input1.get(), pword_input2.get())).place(x=300, y=310)


    def account_validator(self, username_input, pword_input1, pword_input2):
        if self.create_account_warning:
            self.create_account_warning["user"].destroy()
            self.create_account_warning["pword"].destroy()
        self.create_account_warning = {
            "user": Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red"),
            "pword": Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red")
        }

        self.warning_given = {
            "user": False,
            "pword": False
        }

        account_valid = True
        username_exists = self.database_handler.username_exists_check(username_input)

        warning_text = ["Please Enter a Valid Username",
                        "Username Already Exists",
                        "Passwords Don't Match",
                        "Please Enter a Valid Password"]
        conditions = [username_input.strip()=="", username_exists, pword_input1!=pword_input2, pword_input1.strip()==""]
        for i in range(4):
            #warning_type = "user"
            #if i==2 or i==3:
            #    warning_type = "pword"
            warning_type = "pword" if i==2 or i==3 else "user"
            account_valid = self.check_condition(account_valid, conditions[i], warning_text[i], warning_type)


        self.create_account_warning["user"].place(x=250, y=70)
        self.create_account_warning["pword"].place(x=250, y=270)


        if account_valid:
            self.database_handler.create_account(username_input, pword_input1)
            self.create_user_profile()
            #self.sign_in_frame.destroy()
            self.return_to_menu()


    def check_condition(self, account_valid, condition, warning_text, warning_type):
        if condition:
            self.create_account_warning[warning_type].config(text=warning_text)
            self.warning_given[warning_type] = True
            account_valid = False
        else:
            if not self.warning_given[warning_type]:
                self.create_account_warning[warning_type].config(text="")
        return account_valid


    def sign_out(self):
        self.create_guest_profile()
        self.database_handler.user_sign_out()


    def delete_user(self):
        self.create_guest_profile()
        self.database_handler.delete_user()


    def different_log_in(self):
        self.database_handler.user_sign_out()
        self.create_sign_in_frame()


    def switch_eye_image(self, button, pword_input, entry):
        if button.cget("image") == str(self.open_eye):
            button.config(image=self.closed_eye)
            current_input = pword_input.get()
            if entry=="pword":
                self.pword_entry.destroy()
                self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, textvariable=pword_input)
            elif entry=="create_pword":
                self.create_pword_entry.destroy()
                self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, textvariable=pword_input) #may not work, may have to be set to pword_input1
        else:
            button.config(image=self.open_eye)
            current_input = pword_input.get()
            if entry == "pword":
                self.pword_entry.destroy()
                self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
            elif entry == "create_pword":
                self.create_pword_entry.destroy()
                self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input)

        if entry=="pword":
            self.pword_entry.delete(0, len(pword_input.get()) + 1)
            self.pword_entry.insert(0, current_input)
            self.pword_entry.place(x=120, y=160)
        elif entry=="create_pword":
            self.create_pword_entry.delete(0, len(pword_input.get())+1)
            self.create_pword_entry.insert(0, current_input)
            self.create_pword_entry.place(x=150, y=150)


    def change_profile_pic(self):
        colour_options = Menu(self.menu, tearoff=False)
        colours = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
        for colour in colours:
            colour_options.add_command(label="", background=colour, command=lambda current_colour=colour: self.switch_profile_colour(current_colour))
        try:
            x = self.profile_pic.winfo_rootx()
            y = self.profile_pic.winfo_rooty()
            colour_options.tk_popup(x,y+60)
        finally:
            colour_options.grab_release()


    def switch_profile_colour(self, colour):
        self.profile_pic.itemconfig(self.profile_circle, fill=colour)
        #self.database_handler.change_profile_pic_colour(colour)
        self.database_handler.settings.change_profile_pic_colour(colour)