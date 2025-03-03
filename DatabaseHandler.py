import os
from pathlib import Path

class DatabaseHandler:
    def __init__(self):
        self.scores=[]
        self.current_user_file = None
        self.file_lines = None

    def find_user_file(self, username): #returns True if a file of the user's name is found
        directory = "ms_user_data"
        for file in os.listdir(directory):
            if str(file) == f"{username}_classic.txt":
                #self.current_user_file = open(f"/user_data/{username}_classic.txt")
                text_folder = Path("ms_user_data")
                user_file = text_folder / f"{username}_classic.txt"
                self.current_user_file = open(user_file)
                self.file_lines = self.current_user_file.readlines()

                #self.current_user_file = open(f"\ms_user_data\{file}")
                return True
        return False


    def check_password(self, password):
        if str(self.file_lines[0]) == password:
            return True
        return False




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