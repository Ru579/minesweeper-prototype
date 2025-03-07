def find_user_file(self, username):  # returns True if a file of the user's name is found
    directory = "ms_user_data/settings"
    for file in os.listdir(directory):
        if str(file).lower() == f"{username.lower()}_settings.txt":
            username = str(file)[0:len(str(file)) - 13]
            self.username = username
            settings_file = open(f"ms_user_data/settings/{username}_settings.txt")

            settings_data = settings_file.readlines()
            self.pword = settings_data[0].strip("\n")
            self.profile_pic_colour = settings_data[1].strip("\n")
            return True
    return False