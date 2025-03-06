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

        current_user_file = open("ms_user_data/current_user_data.txt")
        lines = current_user_file.readlines()
        if lines:
            self.username = str(lines[0])
            self.profile_pic_colour = str(lines[1])


    #def get_current_user_data(self):
    #    return self.username, self.profile_pic_colour


    def find_user_file(self, username): #returns True if a file of the user's name is found
        directory = "ms_user_data/settings"
        for file in os.listdir(directory):
            if str(file) == f"{username}_settings.txt":
                self.username = username
                #text_folder = Path("ms_user_data/settings")
                #settings_file = text_folder / f"{username}_settings.txt"
                #settings_file = open(settings_file)
                settings_file = open(f"ms_user_data/settings/{username}_settings.txt")

                settings_data = settings_file.readlines()
                self.pword = settings_data[0]
                return True
        return False


    def check_pword(self, password):
        if str(self.pword) == password:
            return True
        return False


    def load_classic_tt_data(self):
        pass


#directory = "ms_user_data"
#        for file in os.listdir(directory):
#            if str(file) == f"{username}_classic.txt":
#                #self.current_user_file = open(f"/user_data/{username}_classic.txt")
#                text_folder = Path("ms_user_data")
#                user_file = text_folder / f"{username}_classic.txt"
#                self.current_user_file = open(user_file)
#                self.file_lines = self.current_user_file.readlines()
#                self.username = username
#
#                #self.current_user_file = open(f"\ms_user_data\{file}")
#                return True
#        return False




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