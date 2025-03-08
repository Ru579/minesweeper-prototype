import os

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

        self.temp_username = ""
        self.temp_profile_pic_colour = ""
        self.temp_pword = ""

        self.top_10_classic = []
        self.top_10_time_trial = []

        #Loads in currently logged-in user, if there is one
        self.current_user_file = open("ms_user_data/current_user_data.txt")
        lines = self.current_user_file.readlines()
        if lines:
            self.username = str(lines[0].strip("\n"))
            self.profile_pic_colour = str(lines[1].strip("\n"))
            self.user_signed_in = True
        else:
            self.user_signed_in = False


    def find_user_file(self, username): #returns True if a file of the user's name is found
        directory = "ms_user_data/settings"
        for file in os.listdir(directory):
            if str(file).lower() == f"{username.lower()}_settings.txt":
                username = str(file)[0:len(str(file))-13]
                self.temp_username = username
                settings_file = open(f"ms_user_data/settings/{username}_settings.txt")

                settings_data = settings_file.readlines()
                self.temp_pword = settings_data[0].strip("\n")
                self.temp_profile_pic_colour = settings_data[1].strip("\n")
                return True
        return False


    def check_pword(self, password):
        if str(self.temp_pword) == password:
            return True
        return False


    def load_classic_tt_data(self):
        pass


    def sign_in_user(self):
        self.username = self.temp_username
        self.pword = self.temp_pword
        self.profile_pic_colour = self.temp_profile_pic_colour
        self.user_signed_in = True
        with open("ms_user_data/current_user_data.txt", "w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")
        with open(f"ms_user_data/classic/{self.username}_Classic.txt") as classic_file:
            data = classic_file.readlines()
            self.top_10_classic = data[0].split(",")
            #for i in range(10):
            #    self.top_10_classic[i] = int(self.top_10_classic[i])
        with open(f"ms_user_data/time_trial/{self.username}_Time_Trial.txt") as tt_file:
            data = tt_file.readlines()
            self.top_10_time_trial = data[0].split(",")
        #converting arrays values from strings into integers
        for i in range(10):
            self.top_10_classic[i] = int(self.top_10_classic[i])
            self.top_10_time_trial[i] = int(self.top_10_time_trial[i])


    def user_sign_out(self):
        with open(f"ms_user_data/settings/{self.username}_settings.txt", "r") as file:
            settings_data = file.readlines()
        settings_data[1] = f"{self.profile_pic_colour}\n"
        with open(f"ms_user_data/settings/{self.username}_settings.txt", "w") as write_file:
            for line in settings_data:
                write_file.write(f"{line}")
        open("ms_user_data/current_user_data.txt","w").close()
        self.user_signed_in = False


    def username_exists_check(self, username):
        directory = "ms_user_data/settings"
        for file in os.listdir(directory):
            if str(file).lower()==f"{username.lower()}_settings.txt":
                return True
        return False


    def create_account(self, username, pword):
        directory = "ms_user_data/settings"
        new_file = f"{username}_settings.txt"
        file_path = os.path.join(directory, new_file)

        with open(file_path, "w") as file:
            file.write(f"{pword}\nred\n")

        game_modes = ["Classic", "Time_Trial"]
        for mode in game_modes:
            #directory = f"ms_user_data/{mode}"
            #new_file = f"{username}_{mode}.txt"
            #file_path = os.path.join(directory, new_file)
            #open(file_path, "w").close()
            with open(f"ms_user_data/{mode}/{username}_{mode}.txt", "w") as file:
                file.write("0,0,0,0,0,0,0,0,0,0")

        self.temp_username = username #set as temp_username because, in self.sign_in(), self.username = self.temp_username
        self.temp_profile_pic_colour = "red" #set as temp_profile_pic_colour for the same reasons as above
        self.sign_in_user()


    def change_profile_pic_colour(self, colour):
        self.profile_pic_colour = colour
        with open("ms_user_data/current_user_data.txt","w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")


    def add_score(self, game_mode, score):
        score = int(score[0:2])*60 + int(score[3:5])
        if game_mode=="Classic":
            self.add_classic_time(score)
        elif game_mode=="Time Trial":
            self.add_tt_stage(score)


    def add_classic_time(self, time):
        with open(f"ms_user_data/classic/{self.username}_Classic.txt", "a") as file:
            file.write(f"{time}\n")



    def add_tt_stage(self, stage):
        with open(f"ms_user_data/time_trial/{self.username}_Classic.txt", "a") as file:
            file.write(f"{stage}\n")


    def check_if_top_10_time(self, time):
        for i in range(0, 10, -1):
            if time>self.top_10_classic[i]:
                if i!=9:
                    self.top_10_classic.insert(i+1, time)
                    del self.top_10_classic[10]
                break


    def check_if_top_10_stage(self, stage):
        for i in range(0,10,-1):
            if stage<self.top_10_time_trial[i]:
                if i!=9:
                    self.top_10_time_trial.insert(i+1, stage)
                    del self.top_10_time_trial[10]
                break














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