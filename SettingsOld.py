class Settings:
    def __init__(self, user_signed_in, username):
        self.user_bool_settings = {}
        self.user_var_settings = {}

        #information about user
        self.username = username
        self.pword = ""

        self.profile_pic_colour = ""

        #all data in the settings file when first loaded
        self.settings_data = []

        self.linked_settings = {
            "Auto Reveal Cells":"Highlight Cells"
        }

        if user_signed_in:
            self.user_signed_in = True
            self.load_user_settings()
        else:
            self.user_signed_in = False
            self.load_guest_settings()
            #self.load_user_settings("guest")


    def load_user_settings(self):
        #sign_in_type="user_log_in"
        #path = f"ms_user_data/Settings/{self.username}_Settings.txt" if user_type=="user_log_in" else "ms_user_data/temp_settings.txt"

        #with open(path) as file:
        #file = open(path)
        file = open(f"ms_user_data/Settings/{self.username}_Settings.txt")
        self.settings_data = file.readlines()

        #loads password profile pic colour
        self.pword = self.settings_data[0].strip("\n")
        self.profile_pic_colour = self.settings_data[1].strip("\n")

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


    def load_guest_settings(self):
        self.username = ""
        self.profile_pic_colour = ""
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


    def create_settings(self, username, pword):
        with open(f"ms_user_data/Settings/{username}_Settings.txt", "w") as file:
            file.write(f"{pword}\n"
                       f"red\n"
                       f"Create Game Finished Window:True\n"
                       f"Auto Reveal Cells:True\n"
                       f"Highlight Cells:True\n"
                       f"Dark Mode:False\n"
                       f"***\n"
                       f"test:10\n")
            # *** is used to separate Boolean settings from settings that can be more than 2 different values (eg. low, medium, high)


    def save_settings(self):
        #pword_and_colour = []
        #if self.user_signed_in:
        #    path = f"ms_user_data/Settings/{self.username}_Settings.txt"
        #    with open(path) as file:
        #        for i in range(2):
        #            pword_and_colour.append(file.readline())
        #else:
        #    path = "ms_user_data/temp_settings.txt"
        path = f"ms_user_data/Settings/{self.username}_Settings.txt" if self.user_signed_in else "ms_user_data/temp_settings.txt"

        with open(path, "w") as file:
            if self.user_signed_in:
                #for line in pword_and_colour:
                #    file.write(line)
                file.write(self.pword + "\n")
                file.write(self.profile_pic_colour + "\n")
            for setting in self.user_bool_settings:
                file.write(f"{setting}:{self.user_bool_settings[setting]}\n")
            file.write("***\n")
            for setting in self.user_var_settings:
                file.write(f"{setting}:{self.user_var_settings[setting]}\n")
            file.close()


    def settings_user_sign_in(self, username):
        self.user_signed_in = True
        self.username = username

        self.load_user_settings()

        #resetting temp_settings
        with open("ms_user_data/temp_settings.txt","w") as file:
            file.write("Create Game Finished Window:True\n"
                       "Auto Reveal Cells:True\n"
                       "Highlight Cells:True\n"
                       "Dark Mode:False\n"
                       "***\n"
                       "test:10\n")
            file.close()


    def settings_user_sign_out(self):
        self.user_signed_in = False
        self.load_guest_settings()


    def change_profile_pic_colour(self, colour):
        self.profile_pic_colour = colour

        #updating profile pic colour in settings file
        with open(f"ms_user_data/Settings/{self.username}_Settings.txt", "w") as file:
            file.write(self.pword + "\n")
            file.write(self.profile_pic_colour + "\n")
            for setting in self.user_bool_settings:
                file.write(f"{setting}:{self.user_bool_settings[setting]}\n")
            file.write("***\n")
            for setting in self.user_var_settings:
                file.write(f"{setting}:{self.user_var_settings[setting]}\n")
            file.close()





