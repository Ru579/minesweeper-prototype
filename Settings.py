class Settings:
    def __init__(self, username):
        self.user_settings = {}

        self.username = username
        self.pword = ""
        self.profile_pic_colour = ""

    def load_user_settings(self, settings_data):
        # loads password and profile pic colour
        self.pword = settings_data[0].strip("\n")
        self.profile_pic_colour = settings_data[1].strip("\n")

        # loads settings
        for i in range(4, len(settings_data)):
            record = settings_data[i].strip("\n").split(":")
            self.user_settings[record[0]] = True if record[1]=="True" else False
        
    def load_guest_settings(self):
        self.username = ""
        self.profile_pic_colour = ""
        # loading the default settings
        self.user_settings = {
            "Create Game Finished Window": True,
            "Enable Chording": True,
            "Highlight Cells when Chording": True
        }
    
    def create_settings(self, username, pword):
        with open(f"ms_user_data/Settings/{username}_Settings.txt", "w") as file:
            file.write(f"{pword}\n"
                       "red\n" \
                       "1\n" \
                       "0\n" \
                       "Create Game Finished Window:True\n" \
                       "Enable Chording:True\n" \
                       "Highlight Cells when Chording:True\n")
        file.close()
    
    def settings_user_sign_in(self, username, settings_data):
        self.user_signed_in = True
        self.username = username
        self.load_user_settings(settings_data)
    
    def settings_user_sign_out(self):
        self.user_signed_in = False
        self.username = ""
        self.load_guest_settings()

    def update_settings_file(self, exp, level):
        with open(f"ms_user_data/Settings/{self.username}_Settings.txt", "w") as settings_file:
            settings_file.write(f"{self.pword}\n"
                                f"{self.profile_pic_colour}\n" \
                                f"{level}\n" \
                                f"{exp}\n" \
                                f"Create Game Finished Window:{self.user_settings["Create Game Finished Window"]}\n" \
                                f"Enable Chording:{self.user_settings["Enable Chording"]}\n" \
                                f"Highlight Cells when Chording:{self.user_settings["Highlight Cells when Chording"]}\n")
        settings_file.close()