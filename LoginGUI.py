from tkinter import *
from PIL import Image, ImageTk
from DatabaseHandler import DatabaseHandler

class LoginGUI:
    def __init__(self, database: DatabaseHandler, minesweeper_window):
        self.database = database # importing the database handler into this class

        # allowing this class to edit the main window and main menu frame
        self.main_window = minesweeper_window
        self.main_menu = Frame() # the actual main menu frame is passed into this class in the create_profile method

        # importing images
        logo = Image.open("Images/mine_cell_red.png")
        logo = logo.resize((150, 150))
        self.logo = ImageTk.PhotoImage(logo)

        open_eye = Image.open("Images/open_eye.png")
        open_eye = open_eye.resize((30, 22))
        self.open_eye = ImageTk.PhotoImage(open_eye)

        closed_eye = Image.open("Images/closed_eye.png")
        closed_eye = closed_eye.resize((30, 22))
        self.closed_eye = ImageTk.PhotoImage(closed_eye)

        guest_pic = Image.open("Images/guest_profile.png")
        guest_pic = guest_pic.resize((60, 60))
        self.guest_image = ImageTk.PhotoImage(guest_pic)

        # Frames
        self.sign_in_frame = Frame()
        self.username_frame = Frame()
        self.pword_frame = Frame()
        
        # GUI widgets
        self.profile_pic = None
        self.profile_circle = None
        self.guest_profile_pic = None
        # sign in widgets
        self.username_entry = None
        self.user_warning_text = None
        self.pword_entry = None
        self.pword_warning_text = None

        # warnings
        self.warning_given = {} # dictionary of which warnings have been given
        self.creation_warning_labels = {} # dictionary of warning labels

        
    
    def create_profile(self, main_menu):
        self.main_menu = main_menu
        
        if self.database.user_signed_in:
           self.create_user_profile()
        else:
            self.create_guest_profile()

    def create_guest_profile(self):
        # destroying the previous profile picture (if there was one)
        if self.profile_pic is not None:
            self.profile_pic.destroy()

        # creating and displaying a guest profile image in corner of main menu
        self.guest_profile_pic = Label(self.main_menu, image=self.guest_image, width=60, height=60)
        self.guest_profile_pic.bind("<Button-1>", lambda _: self.create_account_access_frame("Sign In"))
        self.guest_profile_pic.grid(row=0, column=2)

    
    def create_user_profile(self):
        # destroying the previous profile picture (if there was one)
        if self.profile_pic is not None:
            self.profile_pic.destroy()
        
        # creating profile picture
        self.profile_pic = Canvas(self.main_menu, width=60, height=60, bg="#f0f0f0")
        self.profile_pic.bind("<Button-1>", lambda _: self.show_login_options())
        self.profile_pic.bind("<Button-3>", lambda _: self.show_colour_options())
        self.profile_circle = self.profile_pic.create_oval(3,3,61,61, fill=self.database.settings.profile_pic_colour)
        self.profile_pic.create_text(32, 32, text=self.database.username[0:2], font=("Calibri Bold", 15), anchor="center")
        self.profile_pic.grid(row=0, column=2)

    def create_account_access_frame(self, frame_to_show):
        # swapping frames to the account access frame
        self.sign_in_frame = Frame(self.main_window, width=700, height=440)
        self.main_menu.forget()
        self.sign_in_frame.pack()

        # logo
        logo_label = Label(self.sign_in_frame, image=self.logo, width=150, height=150)
        logo_label.place(x=10, y=140)
        # close button
        Button(self.sign_in_frame, text="X", font=("Calibri", 30), fg="red", command=lambda:self.return_to_menu()).place(x=650, y=0)
        # 'Sign into Minesweeper' text
        Label(self.sign_in_frame, text="Sign into Minesweeper", font=("Calibri", 16)).place(x=10, y=10)

        self.show_account_access_frame(frame_to_show)
    
    def show_account_access_frame(self, frame_to_show, frame_to_destroy=""):
        # destroying previous frame if transitioning between frames
        if frame_to_destroy:
            frame_to_destroy.destroy()
        
        if frame_to_show == "Sign In": # placing the sign in frame
            self.username_sign_in()
        elif frame_to_show == "Create Account": # placing the create an account frame
            self.make_create_account_frame()
    
    def return_to_menu(self):
        self.sign_in_frame.destroy()
        self.main_menu.pack()

    def show_login_options(self):
        log_in_options = Menu(self.main_menu, tearoff=False)
        log_in_options.add_command(label="Sign Out", command=lambda: self.sign_out())
        log_in_options.add_command(label="Sign in with a different account", command=lambda: self.different_log_in())
        log_in_options.add_command(label="Create an Account", command=lambda: self.create_account_access_frame("Create Account"))
        log_in_options.add_command(label="Delete Account", command=lambda: self.show_delete_account_popup())
        
        # displaying the menu
        try:
            x=self.profile_pic.winfo_rootx()
            y=self.profile_pic.winfo_rooty()
            log_in_options.tk_popup(x,y+60)
        finally:
            log_in_options.grab_release()
    
    def sign_out(self):
        self.create_guest_profile()
        self.database.user_sign_out()
    
    def different_log_in(self):
        self.database.user_sign_out()
        self.create_account_access_frame("Sign In")

    def show_delete_account_popup(self):
        # creating a popup to ask if the player truly wishes to delete their account
        deletion_warning = Toplevel()
        deletion_warning.title("Delete Account?")
        Label(deletion_warning, text="Are you sure you want to delete your account- this will remove ALL game data.\n" \
        "This action cannot be reversed.").grid(row=0, column=0)
        Button(deletion_warning, text="DELETE ACCOUNT", font=("Calibri Bold", 16), bg="red",
                   command=lambda:self.delete_account(deletion_warning)).grid(row=1, column=0)
        Button(deletion_warning, text="Cancel", font=("Calibri", 16),
               command=lambda:deletion_warning.destroy()).grid(row=2, column=0)
        
        # making the player only able to click on the popup window until it is closed
        deletion_warning.transient(self.main_window) # keeps popup on top of main window
        deletion_warning.grab_set() # stops interactions with main window
    
    def delete_account(self, deletion_warning_popup):
        deletion_warning_popup.destroy()
        self.database.delete_current_user()
        self.sign_out()

    def show_colour_options(self):
        # preparing a menu of all colours the player can choose from
        colour_options = Menu(self.main_menu, tearoff=False)
        colours = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
        for colour in colours:
            colour_options.add_command(label="", background=colour,
                                       command=lambda current_colour=colour: self.switch_profile_colour(current_colour))
        
        # displaying the menu
        try:
            x = self.profile_pic.winfo_rootx()
            y = self.profile_pic.winfo_rooty()
            colour_options.tk_popup(x,y+60)
        finally:
            colour_options.grab_release()
    
    def switch_profile_colour(self, colour):
        self.profile_pic.itemconfig(self.profile_circle, fill=colour)
        self.database.settings.update_settings_file(new_profile_pic_colour=colour)

    def username_sign_in(self):
        # creating and placing username frame
        self.username_frame = Frame(self.sign_in_frame, width=450, height=350)
        self.username_frame.place(x=175, y=90)

        # making username entry box
        Label(self.username_frame, text="Username:", font=("Calibri", 14)).place(x=15, y=130)
        username_input = StringVar(self.username_frame)
        self.username_entry = Entry(self.username_frame, font=("Calibri", 14), width=25, textvariable=username_input)
        self.username_entry.place(x=120, y=130)

        # making warning text for if the username isn't valid
        self.user_warning_text = Label(self.username_frame, text="", font=("Calibri Bold", 11), fg="red")
        self.user_warning_text.place(x=260, y=190)

        # Create Account and Continue buttons at bottom of screen
        Button(self.username_frame, text="Create Account?", font=("Calibri Bold", 13), fg="#258cdb",
               command=lambda: self.make_create_account_frame(frame_to_forget=self.username_frame)).place(x=180, y=310)
        Button(self.username_frame, text="Continue", font=("Calibri Bold", 13), bg="#258cdb",
               command=lambda: self.confirm_username(username_input.get())).place(x=330, y=310)

    def confirm_username(self, username_input):
        if username_input.strip()=="": # if no username has been entered (ignoring whitespace)
            self.user_warning_text.config(text="Please Enter a Username")
        elif not self.database.find_user_file(username_input): # if username doesn't exist
            self.user_warning_text.config(text="Username not found")
        else: # valid username entered
            self.pword_sign_in()

    def pword_sign_in(self):
        # switching username and password sign in frame
        self.username_frame.forget()
        self.pword_frame = Frame(self.sign_in_frame, width=450, height=350)
        self.pword_frame.place(x=175, y=90)

        # dispalying previously entered username
        Label(self.pword_frame, text=f"Username: {self.database.temp_username}", font=("Calibri", 12)).place(x=15, y=130)
        
        # making password entry box
        Label(self.pword_frame, text="Password:", font=("Calibri", 14)).place(x=15, y=160)
        pword_input = StringVar(self.pword_frame)
        self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
        self.pword_entry.place(x=120, y=160)

        # making 'eye' icon that hides or reveals pword
        view_pword_toggle = Button(self.pword_frame, image=self.open_eye, width=30, height=22,
                                   command=lambda: self.switch_eye_image(view_pword_toggle, pword_input, "pword"))
        view_pword_toggle.place(x=380, y=160)

        # making warning text for if the password isn't correct
        self.pword_warning_text = Label(self.pword_frame, text="", font=("Calibri Bold", 11), fg="red")
        self.pword_warning_text.place(x=260, y=220)

        # Sign in and 'back to username sign in' buttons
        Button(self.pword_frame, text="Sign In", font=("Calibri Bold", 13), bg="#258cdb",
               command=lambda: self.confirm_pword(pword_input.get())).place(x=330, y=310)
        Button(self.pword_frame, text="Back", font=("Calibri Bold", 13), fg="black",
               command=lambda: self.back_to_username_frame()).place(x=180, y=310)

    def confirm_pword(self, pword_input):
        pword_correct = self.database.check_pword(pword_input)
        
        if pword_correct:
            self.database.sign_in_user()
            self.create_user_profile()
            self.return_to_menu()
        else:
            self.pword_warning_text.config(text="Incorrect Password")
    
    def back_to_username_frame(self):
        # destroying the password frame and showing the username frame again
        self.pword_frame.destroy()
        self.username_frame.place(x=175, y=90)
    
    def make_create_account_frame(self, frame_to_forget=""):
        # hiding the previous frame if there was one
        if frame_to_forget:
            frame_to_forget.forget()

        self.create_account_frame = Frame(self.sign_in_frame, width=550, height=350)
        self.create_account_frame.place(x=175, y=90)

        # creating entry box for username
        Label(self.create_account_frame, text="Username:", font=("Calibri", 12)).place(x=50, y=50)
        username_input = StringVar(self.create_account_frame)
        username_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, textvariable=username_input)
        username_entry.place(x=150, y=50)

        # creating entry box for 1st input of password
        Label(self.create_account_frame, text="Password:", font=("Calibri", 12)).place(x=50, y=150)
        pword_input1 = StringVar(self.create_account_frame)
        self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input1)
        self.create_pword_entry.place(x=150, y=150)
        # adding 'eye' icon for hiding or revealing password
        view_create_pword_toggle = Button(self.create_account_frame, image=self.open_eye, width=30, height=22,
                                          command=lambda: self.switch_eye_image(view_create_pword_toggle, pword_input1, "create_pword"))
        view_create_pword_toggle.place(x=360, y=150)

        # creating entry box for 2nd input of password (confirm password box)
        Label(self.create_account_frame, text="Confirm Password:", font=("Calibri", 12)).place(x=10, y=250)
        pword_input2 = StringVar(self.create_account_frame)
        self.confirm_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input2)
        self.confirm_pword_entry.place(x=150, y=250)

        # button for going back to username sign in frame or for officially creating the account
        Button(self.create_account_frame, text="Sign In", font=("Calibri Bold", 13), fg="#258cdb",
               command=lambda: self.show_account_access_frame("Sign In", self.create_account_frame)).place(x=220, y=310)
        Button(self.create_account_frame, text="Create Account", font=("Calibri Bold", 13), bg="#258cdb",
               command=lambda: self.account_validator(username_input.get(), pword_input1.get(), pword_input2.get())).place(x=300, y=310)
    
    def account_validator(self, username_input, pword_input1, pword_input2):
        # removing old Labels and making new ones
        if self.creation_warning_labels:
            self.creation_warning_labels["user"].destroy()
            self.creation_warning_labels["pword"].destroy()
        self.creation_warning_labels = {
            "user": Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red"),
            "pword": Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red")
        }

        # resetting whether warnings have been given yet
        self.warning_given = {
            "user": False,
            "pword": False
        }

        account_valid = True # assume details are valid until proven otherwise

        # each condition maps to the warning displayed if it is met
        warning_text = ["Please Enter a Valid Username",
                        "Username Already Exists",
                        "Passwords Don't Match",
                        "Please Enter a Valid Password"]
        conditions = [username_input.strip()=="",
                      self.database.username_exists_check(username_input),
                      pword_input1!=pword_input2,
                      pword_input1.strip()==""]
        

        # checking if any of the above conditions are met, in which case invalidating account creation
        for i in range(4):
            warning_type = "pword" if i==2 or i==3 else "user"
            account_valid = self.check_condition(account_valid, conditions[i], warning_text[i], warning_type)
        
        self.creation_warning_labels["user"].place(x=250, y=70)
        self.creation_warning_labels["pword"].place(x=250, y=270)

        # creates an account and signs in user if account details are valid
        if account_valid:
            self.database.create_account(username_input, pword_input1)
            self.create_user_profile()
            self.return_to_menu()
    
    def check_condition(self, account_valid, condition, warning_text, warning_type):
        if condition:
            # if the condition was met, show the corresponding warning text to user, account details no longer valid
            self.creation_warning_labels[warning_type].config(text=warning_text)
            self.warning_given[warning_type] = True
            account_valid = False
        elif not self.warning_given[warning_type]: 
            # resetting the warning text label to be blank if a warning hasn't been given at all
            self.creation_warning_labels[warning_type].config(text="")
        
        return account_valid

    def switch_eye_image(self, button, pword_input, entry_type):
        current_input = pword_input.get() # retrieving what the user has currently entered into the Entry box for reinsertion later
        if button.cget("image") == str(self.open_eye): # if eye icon is open- password is currently hidden
            button.config(image=self.closed_eye)
            
            # destroys the appropriate Entry box and then replaces it with one with all characters showing
            if entry_type=="pword":
                self.pword_entry.destroy()
                self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, textvariable=pword_input)
            elif entry_type=="create_pword":
                self.create_pword_entry.destroy()
                self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, textvariable=pword_input)
        
        else: # if eye icon is closed- password is currently showing
            button.config(image=self.open_eye)

            # destroys the appropriate Entry box and then replaces it with one with all characters represented as *s
            if entry_type == "pword":
                self.pword_entry.destroy()
                self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
            elif entry_type == "create_pword":
                self.create_pword_entry.destroy()
                self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input)

        # removing the old contents of the Entry box and then re-inserting the user's inputs (now either hidden as *s or shown normally)
        # this is different to previously destroying the Entry box itself, which preserves Entry contents 
        if entry_type=="pword":
            self.pword_entry.delete(0, len(pword_input.get()) + 1) # removing the old contents of the Entry box
            self.pword_entry.insert(0, current_input)
            self.pword_entry.place(x=120, y=160)
        elif entry_type=="create_pword":
            self.create_pword_entry.delete(0, len(pword_input.get())+1)
            self.create_pword_entry.insert(0, current_input)
            self.create_pword_entry.place(x=150, y=150)
