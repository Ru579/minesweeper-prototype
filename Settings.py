class Settings:
    def __init__(self, username, user_signed_in):
        self.user_settings = {}

        self.username = username
        self.pword = ""
        self.profile_pic_colour = ""
        self.level = 0
        self.exp = 0

        # the 'value' is the setting dependent on the 'key'- ie. the value can only be True if the key is
        self.linked_settings = {
            "Enable Chording":"Highlight Cells when Chording"
        }

        # loading currently logged-in player's settings, otherwise loading default settings
        if user_signed_in:
            self.user_signed_in = True
            self.load_user_settings()
        else:
            self.user_signed_in = False
            self.load_guest_settings()

    def load_user_settings(self, settings_data=[], exp=None, level=None):
        # reading settings from file if file data wasn't passed in
        if not settings_data:
            with open(f"ms_user_data/Settings/{self.username}_Settings.txt") as settings_file:
                settings_data = settings_file.readlines()
            settings_file.close()
        
        # loads password, profile pic colour, player level and player EXP
        self.pword = settings_data[0].strip("\n")
        self.profile_pic_colour = settings_data[1].strip("\n")
        self.level = level if level else settings_data[2].strip("\n")
        self.exp = exp if exp else settings_data[3].strip("\n")
        
        # loads settings into attributes
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
    
    def settings_user_sign_in(self, username, settings_data, exp, level):
        self.user_signed_in = True
        self.username = username
        
        self.load_user_settings(settings_data, exp, level)
    
    def settings_user_sign_out(self):
        self.user_signed_in = False
        self.username = ""
        self.load_guest_settings()

    def update_settings_file(self, new_exp="", new_level="", new_profile_pic_colour=""):
        # updating attributes if any new values for these attributes are passed into the method, otherwise keeping them the same as before
        self.exp = new_exp if new_exp else self.exp
        self.level = new_level if new_level else self.level
        self.profile_pic_colour = new_profile_pic_colour if new_profile_pic_colour else self.profile_pic_colour
        
        # writing settings and new player data to file
        with open(f"ms_user_data/Settings/{self.username}_Settings.txt", "w") as settings_file:
            settings_file.write(f"{self.pword}\n"
                                f"{self.profile_pic_colour}\n" \
                                f"{self.level}\n" \
                                f"{self.exp}\n" \
                                f"Create Game Finished Window:{self.user_settings["Create Game Finished Window"]}\n" \
                                f"Enable Chording:{self.user_settings["Enable Chording"]}\n" \
                                f"Highlight Cells when Chording:{self.user_settings["Highlight Cells when Chording"]}\n")
        settings_file.close()
    
    def switch_setting(self, setting_name):
        # returns the name of the linked setting whose switch must be updated if there is one
        if not self.user_settings[setting_name]: # if setting is currently False
            self.user_settings[setting_name] = True

            if setting_name in self.linked_settings.values(): # if this setting is dependent on another
                # finding the key that setting_name is dependent on and also setting it to True
                for setting_key in self.linked_settings.keys():
                    if self.linked_settings[setting_key] == setting_name:
                        linked_setting = setting_key
                        self.user_settings[linked_setting] = True
                return linked_setting
            return None

        else: # setting is currently True
            self.user_settings[setting_name] = False
            if setting_name in self.linked_settings.keys(): # if another setting is dependent on this one
                # also switching the dependent setting to False
                self.user_settings[self.linked_settings[setting_name]] = False
                return self.linked_settings[setting_name]
            return None
    
