def account_validator(self, username_input, pword_input1, pword_input2):
    # self.create_account_warning = {
    #    "user": Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red"),
    #    "pword": Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red")
    # }
    if self.create_account_warning:
        self.create_account_warning[0].destroy()
        self.create_account_warning[1].destroy()
    self.create_account_warning = [Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red"), Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red")]

    self.warning_given = {
        "user": False,
        "pword": False
    }

    # self.create_account_warning["user"].place(x=250, y=70)
    # self.create_account_warning["pword"].place(x=250, y=270)

    account_valid = True
    username_exists = self.database_handler.username_exists_check(username_input)

    warning_text = ["Please Enter a Valid Username",
                    "Username Already Exists",
                    "Passwords Don't Match",
                    "Please Enter a Valid Password"]
    conditions = [username_input.strip() == "", username_exists, pword_input1 != pword_input2, pword_input1.strip() == ""]
    print(f"conditions are: {conditions}")
    for i in range(4):
        warning_type = 0
        if i == 2 or i == 3:
            warning_type = 1
        account_valid = self.check_condition(account_valid, conditions[i], warning_text[i], warning_type)

    self.create_account_warning[0].place(x=250, y=70)
    self.create_account_warning[1].place(x=250, y=270)

    if account_valid:
        self.database_handler.create_account(username_input, pword_input1)
        self.create_user_profile()
        self.sign_in_window.destroy()


def check_condition(self, account_valid, condition, warning_text, warning_type):
    if warning_type == 0:
        current_type = "user"
    else:
        current_type = "pword"
    if condition:
        self.create_account_warning[warning_type].config(text=warning_text)
        self.warning_given[current_type] = True
        account_valid = False
    else:
        if not self.warning_given[current_type]:
            print(f"No {warning_type} warnings given")
            self.create_account_warning[warning_type].config(text="")
            # self.create_account_warning[warning_type].destroy()
            # self.create_account_warning[warning_type] = Label(self.create_account_frame, font=("Calibri Bold", 12), fg="red")
    return account_valid