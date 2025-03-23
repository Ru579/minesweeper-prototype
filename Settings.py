class Settings:
    def __init__(self, user_signed_in, username):
        self.user_bool_settings = {}
        self.user_var_settings = {}

        self.username = username

        # settings data
        self.settings_data = []

        self.linked_settings = {
            "Auto Reveal Cells":"Highlight Cells"
        }

        if user_signed_in:
            self.user_signed_in = True
            self.load_user_settings()
        else:
            self.user_signed_in = False
            self.load_default_settings()


    def load_user_settings(self):
        with open(f"ms_user_data/Settings/{self.username}_Settings.txt") as file:
            self.settings_data = file.readlines()

            # loads boolean settings
            i = 2
            while self.settings_data[i] != "***\n":
                record = self.settings_data[i].strip("\n").split(":")
                if record[1] == "True":
                    self.user_bool_settings[record[0]] = True
                elif record[1] == "False":
                    self.user_bool_settings[record[0]] = False
                i += 1

            # loads variable settings
            for j in range(i + 1, len(self.settings_data) - 1):
                record = self.settings_data[j].strip("\n").split(":")
                self.user_var_settings[record[0]] = record[1]


    def load_default_settings(self):
        self.user_bool_settings = {
            "Create Game Finished Window": True,
            "Auto Reveal Cells": True, # auto reveal a 'full' cell when it is clicked
            "Highlight Cells": True, # highlights cells purple when there is a non-zero flag difference
            "Dark Mode": False
        }
        self.user_var_settings = {
            "test": "10"
        }


    def switch(self, bool_setting):
        if not self.user_bool_settings[bool_setting]:
            self.user_bool_settings[bool_setting] = True
            if bool_setting in self.linked_settings.values():
                linked_key = [key for key, val in self.linked_settings.items() if val==bool_setting][0]
                self.user_bool_settings[linked_key] = True
                return linked_key
            return None

        else:
            self.user_bool_settings[bool_setting] = False
            if bool_setting in self.linked_settings:
                self.user_bool_settings[self.linked_settings[bool_setting]] = False #also switches the linked setting to False
                return self.linked_settings[bool_setting]
            return None



    #def save_settings(self):
    #    if self.user_signed_in:
    #        pword_and_colour = []
    #        with open(f"ms_user_data/Settings/{self.username}_Settings.txt") as file:
    #            for i in range(2):
    #                pword_and_colour.append(file.readline())
    #        with open(f"ms_user_data/Settings/{self.username}_Settings.txt", "w") as file:
    #            for line in pword_and_colour:
    #                file.write(line)
    #            for setting in self.user_bool_settings:
    #                file.write(f"{setting}:{self.user_bool_settings[setting]}\n")
    #            for setting in self.user_var_settings:
    #                file.write(f"{setting}:{self.user_var_settings[setting]}\n")
    #            file.close()
    #    else:

    def save_settings(self):
        pword_and_colour = []
        if self.user_signed_in:
            path = f"ms_user_data/Settings/{self.username}_Settings.txt"
            with open(path) as file:
                for i in range(2):
                    pword_and_colour.append(file.readline())
        else:
            path = "ms_user_data/temp_settings.txt"

        with open(path, "w") as file:
            if self.user_signed_in:
                for line in pword_and_colour:
                    file.write(line)
            for setting in self.user_bool_settings:
                file.write(f"{setting}:{self.user_bool_settings[setting]}\n")
            for setting in self.user_var_settings:
                file.write(f"{setting}:{self.user_var_settings[setting]}\n")
            file.close()


    def settings_user_sign_out(self):
        self.user_signed_in = False
        



