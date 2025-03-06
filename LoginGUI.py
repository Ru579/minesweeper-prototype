from tkinter import *
from PIL import Image, ImageTk
from DatabaseHandler import *

class LoginGUI():
    def __init__(self, menu):
        self.menu = menu

        logo = Image.open("mine_cell_red.png")
        logo = logo.resize((150, 150))
        self.logo = ImageTk.PhotoImage(logo)

        open_eye = Image.open("open_eye.png")
        open_eye = open_eye.resize((30, 22))
        self.open_eye = ImageTk.PhotoImage(open_eye)

        closed_eye = Image.open("closed_eye.png")
        closed_eye = closed_eye.resize((30, 22))
        self.closed_eye = ImageTk.PhotoImage(closed_eye)

        pic = Image.open("guest_profile.png")
        pic = pic.resize((60, 60))
        self.guest_image = ImageTk.PhotoImage(pic)

        self.database_handler = DatabaseHandler()

        #frames and windows
        self.login_frame = Frame(menu)
        self.login_frame.grid(row=0, column=2)
        self.sign_in_window = None
        self.username_frame = None
        self.pword_frame = None

        #other widgets
        self.profile_pic = None
        self.guest_profile_pic = None
        self.username_entry = None
        self.user_warning_text=None
        self.pword_entry = None
        self.pword_warning_text = None

        self.login_button = Button(self.login_frame, font=("Calibri", 15), height=2, width=15, command=lambda: self.log_in())
        self.login_button.grid(row=0, column=1)

        if self.database_handler.username=="":
            self.signed_in = False
            self.create_guest_profile()
        else:
            self.signed_in = True
            self.create_user_profile()


    def create_guest_profile(self):
        # EXPERIMENTAL
        if self.profile_pic is not None:
            self.profile_pic.destroy()


        self.guest_profile_pic = Label(self.login_frame, image=self.guest_image, width=60, height=60)
        self.guest_profile_pic.grid(row=0, column=0)
        self.login_button.config(text="Log In")
        self.login_button.grid(row=0, column=1)


    def create_user_profile(self):
        #EXPERIMENTAL
        if self.profile_pic is not None:
            self.profile_pic.destroy()

        #creating profile picture
        self.profile_pic = Canvas(self.login_frame, width=60, height=60, bg="#f0f0f0")
        self.profile_pic.create_oval(3,3,61,61, fill=self.database_handler.profile_pic_colour)
        self.profile_pic.create_text(32, 32, text=self.database_handler.username[0:2], font=("Calibri Bold", 15), anchor="center")
        self.profile_pic.grid(row=0, column=0)
        #creating login button
        if len(self.database_handler.username)>15:
            username = self.database_handler.username[0:16]
        else:
            username = self.database_handler.username
        self.login_button.config(text=username)


    def clear_login_frame(self):
        for widget in self.login_frame:
            widget.destroy()


    def log_in(self):
        if self.login_button.cget("text")!="Log In":
            log_in_options = Menu(self.menu, tearoff=False)
            log_in_options.add_command(label="Sign Out", command=lambda: self.sign_out())
            log_in_options.add_command(label="Sign in with a different account", command=lambda: self.different_log_in())
            try:
                x=self.login_button.winfo_rootx()
                y=self.login_button.winfo_rooty()
                log_in_options.tk_popup(x,y+10)
            finally:
                log_in_options.grab_release()
        else:
            self.sign_in()


    def sign_in(self):
        self.sign_in_window = Toplevel(self.menu)
        self.sign_in_window.title("Sign In")
        self.sign_in_window.geometry("600x400")

        logo_label = Label(self.sign_in_window, image=self.logo, width=150,height=150)
        logo_label.place(x=10, y=110)

        Label(self.sign_in_window, text="Sign into Minesweeper", font=("Calibri", 16)).place(x=10, y=10)

        self.username_sign_in()


    def username_sign_in(self):
        self.username_frame = Frame(self.sign_in_window, width=450, height=350)
        self.username_frame.place(x=175, y=50)

        Label(self.username_frame, text="Username:", font=("Calibri", 14)).place(x=15, y=130)
        username_input = StringVar(self.username_frame)
        self.username_entry = Entry(self.username_frame, font=("Calibri", 14), width=25, textvariable=username_input)
        self.username_entry.place(x=120, y=130)

        self.user_warning_text = Label(self.username_frame, text="", font=("Calibri", 11), fg="red")
        self.user_warning_text.place(x=260, y=190)

        Button(self.username_frame, text="Create Account?", font=("Calibri Bold", 13), fg="#258cdb",
               command=lambda: self.create_account()).place(x=180, y=310)
        Button(self.username_frame, text="Continue", font=("Calibri Bold", 13), bg="#258cdb",
               command=lambda: self.confirm_username(username_input.get())).place(x=330, y=310)


    def confirm_username(self, username_input):
        username_found = self.database_handler.find_user_file(username_input.lower())
        if not username_found:
            self.user_warning_text.config(text="Username not found")
        else:
            self.pword_sign_in()


    def pword_sign_in(self):
        # switching username with password sign in frame
        self.username_frame.forget()
        self.pword_frame = Frame(self.sign_in_window, width=450, height=350)
        self.pword_frame.place(x=175, y=50)

        Label(self.pword_frame, text=f"Username: {self.database_handler.username}", font=("Calibri", 12)).place(x=15, y=130)
        Label(self.pword_frame, text="Password:", font=("Calibri", 14)).place(x=15, y=160)

        pword_input = StringVar(self.pword_frame)
        self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
        self.pword_entry.place(x=120, y=160)

        view_pword_toggle = Button(self.pword_frame, image=self.open_eye, width=30, height=22,
                                   command=lambda: self.switch_eye_image(view_pword_toggle, pword_input))
        view_pword_toggle.place(x=380, y=160)

        self.pword_warning_text = Label(self.pword_frame, text="", font=("Calibri", 11), fg="red")
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
            self.create_user_profile()
            self.sign_in_window.destroy()


    def back_to_username_frame(self):
        self.pword_frame.destroy()
        self.username_frame.place(x=175,y=50)


    def create_account(self):
        pass


    def sign_out(self):
        pass


    def different_log_in(self):
        pass


    def switch_eye_image(self, button, pword_input):
        if button.cget("image") == str(self.open_eye):
            button.config(image=self.closed_eye)
            current_input = pword_input.get()
            self.pword_entry.destroy()
            self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, textvariable=pword_input)
            #self.pword_entry.delete(0, len(pword_input.get()) + 1)
            #self.pword_entry.insert(0, current_input)
            #self.pword_entry.place(x=120, y=160)
        else:
            button.config(image=self.open_eye)
            current_input = pword_input.get()
            self.pword_entry.destroy()
            self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
        self.pword_entry.delete(0, len(pword_input.get()) + 1)
        self.pword_entry.insert(0, current_input)
        self.pword_entry.place(x=120, y=160)