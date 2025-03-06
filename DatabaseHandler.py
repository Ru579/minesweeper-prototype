import os
from pathlib import Path

class DatabaseHandler:
    def __init__(self):
        self.scores=[]
        self.current_user_file = None
        self.classic_data = None
        self.tt_data = None
        #self.file_lines = None
        self.username = ""
        self.profile_pic_colour=""
        self.pword=""

        #attempts to read username and profile pic colour from current user file
        #data_folder = Path("ms_user_data")
        #current_user_file = data_folder / "current_user_data"
        #current_user_file = open(current_user_file)

        self.current_user_file = open("ms_user_data/current_user_data.txt")
        lines = self.current_user_file.readlines()
        if lines:
            self.username = str(lines[0].strip("\n"))
            self.profile_pic_colour = str(lines[1].strip("\n"))


    #def get_current_user_data(self):
    #    return self.username, self.profile_pic_colour


    #SHOULDN@T COMPLETELY LOAD IN USER'S FILES YET UNTIL CONFIRMED THAT THEY HAVE SIGNED IN

    def find_user_file(self, username): #returns True if a file of the user's name is found
        directory = "ms_user_data/settings"
        for file in os.listdir(directory):
            if str(file) == f"{username}_settings.txt":
                self.username = username
                settings_file = open(f"ms_user_data/settings/{username}_settings.txt")

                settings_data = settings_file.readlines()
                self.pword = settings_data[0].strip("\n")
                self.profile_pic_colour = settings_data[1].strip("\n")
                return True
        return False


    def check_pword(self, password):
        if str(self.pword) == password:
            return True
        #print(f"self.pword = {self.pword} and user's input = {password}")
        return False


    def load_classic_tt_data(self):
        pass


    def user_signed_in(self):
        with open("ms_user_data/current_user_data.txt", "w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")


    def user_sign_out(self):
        with open(f"ms_user_data/settings/{self.username}_settings.txt", "r") as file:
            settings_data = file.readlines()
        #settings_data[0] = self.pword #this line can be removed if we don't implement a feature allowing the user to change their password
        settings_data[1] = f"{self.profile_pic_colour}\n"
        with open(f"ms_user_data/settings/{self.username}_settings.txt", "w") as write_file:
            for line in settings_data:
                write_file.write(f"{line}")
        open("ms_user_data/current_user_data.txt","w").close()


    def username_exists_check(self, username):
        directory = "ms_user_data/settings"
        for file in os.listdir(directory):
            if str(file)==f"{username}_settings.txt":
                return True
        return False


    def create_account(self, username, pword):
        directory = "ms_user_data/settings"
        new_file = f"{username}_settings.txt"
        file_path = os.path.join(directory, new_file)

        with open(file_path, "w") as file:
            file.write(f"{pword}\nred\n")

        game_modes = ["classic", "time_trial"]
        for mode in game_modes:
            directory = f"ms_user_data/{mode}"
            new_file = f"{username}_{mode}.txt"
            file_path = os.path.join(directory, new_file)
            open(file_path, "w").close()

        self.username = username
        self.profile_pic_colour = "red"
        self.user_signed_in()










#import datetime
#scores = {}
#leaderboard = {}
#def add_classic_user_info(username, time):  # where time is an array, 1st index is minutes, 2nd index is seconds
#    with open("scores.txt", "r") as file:
#        for line in file:
#            record = line.split(":")
#            scores[f"{record[0]}"] = record[1].strip("\n")
#    date = datetime.datetime.now().strftime("%x").split("/")
#    scores[f"{username}({date[1]}-{date[0]}-{date[2]})"] = f"{time[0]}-{time[1]}"
#    with open("scores.txt", "w") as file:
#        for a, b in scores.items():
#            file.write(f"{a}:{b}\n")
#
##for the future, could keep track of what records are new, and then open the file using "a" instead of "w"
## to append the new records to the end of the file instead of writing the whole file again
#
#
#def organise_scores():
#    with open("scores.txt", "r") as file:
#        for line in file:
#            record = line.split(":")
#            scores[f"{record[0]}"] = record[1].strip("\n")
#    for name, time in scores.items():
#        leaderboard[name] = str(time[0:2]) + str(time[3:5])
#    sorted_list = dict(sorted(leaderboard.items(), key=lambda item: item[1]))
#    print(sorted_list)  # CHECKING LINE