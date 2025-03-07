def switch_eye_image(self, button, pword_input, entry):
    if button.cget("image") == str(self.open_eye):
        button.config(image=self.closed_eye)
        current_input = pword_input.get()
        if entry == "pword":
            self.pword_entry.destroy()
            self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, textvariable=pword_input)
        elif entry == "create_pword":
            self.create_pword_entry.destroy()
            self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, textvariable=pword_input)  # may not work, may have to be set to pword_input1
        elif entry == "confirm_pword":
            self.confirm_pword_entry.destroy()
            self.confirm_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, textvariable=pword_input)  # may not work, may have to be set to pword_input2
    else:
        button.config(image=self.open_eye)
        current_input = pword_input.get()
        # self.pword_entry.destroy()
        # self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
        if entry == "pword":
            self.pword_entry.destroy()
            self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
        elif entry == "create_pword":
            self.create_pword_entry.destroy()
            self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input)
        elif entry == "confirm_pword":
            self.confirm_pword_entry.destroy()
            self.confirm_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input)
    self.pword_entry.delete(0, len(pword_input.get()) + 1)
    self.pword_entry.insert(0, current_input)
    self.pword_entry.place(x=120, y=160)





def switch_eye_image(self, button, pword_input, entry):
    if button.cget("image") == str(self.open_eye):
        button.config(image=self.closed_eye)
        current_input = pword_input.get()
        if entry == "pword":
            self.pword_entry.destroy()
            self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, textvariable=pword_input)
        elif entry == "create_pword":
            self.create_pword_entry.destroy()
            self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, textvariable=pword_input)  # may not work, may have to be set to pword_input1
        elif entry == "confirm_pword":
            self.confirm_pword_entry.destroy()
            self.confirm_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, textvariable=pword_input)  # may not work, may have to be set to pword_input2
    else:
        button.config(image=self.open_eye)
        current_input = pword_input.get()
        # self.pword_entry.destroy()
        # self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
        if entry == "pword":
            self.pword_entry.destroy()
            self.pword_entry = Entry(self.pword_frame, font=("Calibri", 14), width=25, show="*", textvariable=pword_input)
        elif entry == "create_pword":
            self.create_pword_entry.destroy()
            self.create_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input)
        elif entry == "confirm_pword":
            self.confirm_pword_entry.destroy()
            self.confirm_pword_entry = Entry(self.create_account_frame, font=("Calibri", 12), width=25, show="*", textvariable=pword_input)
    if entry == "pword":
        self.pword_entry.delete(0, len(pword_input.get()) + 1)
        self.pword_entry.insert(0, current_input)
        self.pword_entry.place(x=120, y=160)
    elif entry == "create_pword":
        self.create_pword_entry.delete(0, len(pword_input.get()) - 1)
        self.create_pword_entry.insert(0, current_input)
        self.create_pword_entry.place(x=410, y=150)
    elif entry == "confirm_pword":
        self.confirm_pword_entry.delete(0, len(pword_input.get()) - 1)
        self.confirm_pword_entry.insert(0, current_input)
        self.confirm_pword_entry.place(x=410, y=250)