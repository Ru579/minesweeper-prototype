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
        self.no_of_games = 0
        self.no_of_losses = 0
        self.boards_completed = 0

        self.temp_username = ""
        self.temp_profile_pic_colour = ""
        self.temp_pword = ""
        #self.temp_no_of_games = 0
        #self.temp_no_of_losses = 0
        #self.temp_boards_completed = 0

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
        directory = "ms_user_data/Settings"
        for file in os.listdir(directory):
            if str(file).lower() == f"{username.lower()}_Settings.txt":
                username = str(file)[0:len(str(file))-13]
                self.temp_username = username
                settings_file = open(f"ms_user_data/Settings/{username}_Settings.txt")

                settings_data = settings_file.readlines()
                self.temp_pword = settings_data[0].strip("\n")
                self.temp_profile_pic_colour = settings_data[1].strip("\n")
                #games_losses_boards = settings_data[2].strip("\n").split(",")
                #self.temp_no_of_games = int(games_losses_boards[0])
                #self.temp_no_of_losses = int(games_losses_boards[1])
                #self.temp_boards_completed = int(games_losses_boards[2])
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
        #self.no_of_games = self.temp_no_of_games
        #self.no_of_losses = self.temp_no_of_losses
        #self.boards_completed = self.temp_boards_completed
        with open(f"ms_user_data/Settings/{self.username}_Settings.txt") as file:
            settings_data = file.readlines()
            games_losses_boards = settings_data[2].strip("\n").split(",")
        self.no_of_games = int(games_losses_boards[0])
        self.no_of_losses = int(games_losses_boards[1])
        self.boards_completed = int(games_losses_boards[2])
        self.user_signed_in = True
        with open("ms_user_data/current_user_data.txt", "w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")
        with open(f"ms_user_data/Classic/{self.username}_Classic.txt") as classic_file:
            data = classic_file.readlines()
            self.top_10_classic = data[0].split(",")
            #for i in range(10):
            #    self.top_10_classic[i] = int(self.top_10_classic[i])
        with open(f"ms_user_data/Time Trial/{self.username}_Time Trial.txt") as tt_file:
            data = tt_file.readlines()
            self.top_10_time_trial = data[0].split(",")
        #converting arrays values from strings into integers
        for i in range(10):
            self.top_10_classic[i] = int(self.top_10_classic[i])
            self.top_10_time_trial[i] = int(self.top_10_time_trial[i])


    def user_sign_out(self):
        with open(f"ms_user_data/Settings/{self.username}_Settings.txt", "r") as file:
            settings_data = file.readlines()
        settings_data[1] = f"{self.profile_pic_colour}\n"
        with open(f"ms_user_data/Settings/{self.username}_Settings.txt", "w") as write_file:
            for line in settings_data:
                write_file.write(f"{line}")
        open("ms_user_data/current_user_data.txt","w").close()
        self.user_signed_in = False


    def username_exists_check(self, username):
        directory = "ms_user_data/Settings"
        for file in os.listdir(directory):
            if str(file).lower()==f"{username.lower()}_Settings.txt":
                return True
        return False


    def create_account(self, username, pword):
        #directory = "ms_user_data/settings"
        #new_file = f"{username}_settings.txt"
        #file_path = os.path.join(directory, new_file)

        #with open(file_path, "w") as file:
        #    file.write(f"{pword}\nred\n0,0,0\n")

        with open(f"ms_user_data/Settings/{username}_Settings.txt", "w") as file:
            file.write(f"{pword}\nred\n0,0,0\n")

        #game_modes = ["Classic", "Time Trial"]
        #for mode in game_modes:
        #    with open(f"ms_user_data/{mode}/{username}_{mode}.txt", "w") as file:
        #        file.write("0,0,0,0,0,0,0,0,0,0\n")

        with open(f"ms_user_data/Time Trial/{username}_Time Trial.txt","w") as file:
            file.write("0,0,0,0,0,0,0,0,0,0")

        difficulties = ["Beginner", "Intermediate", "Expert"]
        for difficulty in difficulties:
            with open(f"ms_user_data/Classic/{difficulty}/{username}_ClBeginner.txt","w") as file:
                file.write("0,0,0,0,0,0,0,0,0,0")
        # Cl is put before the difficulty to signify that this is a classic game mode- just in case, in the future, other game modes are introduced that use game modes

        self.temp_username = username #set as temp_username because, in self.sign_in(), self.username = self.temp_username
        self.temp_profile_pic_colour = "red" #set as temp_profile_pic_colour for the same reasons as above
        self.sign_in_user()


    def change_profile_pic_colour(self, colour):
        self.profile_pic_colour = colour
        with open("ms_user_data/current_user_data.txt","w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")


    #def add_score(self, game_mode, score):
    #    #score = int(score[0:2])*60 + int(score[3:5])
    #    if game_mode=="Classic":
    #        score = int(score[0:2]) * 60 + int(score[3:5])
    #        self.add_classic_time(score)
    #    elif game_mode=="Time Trial":
    #        self.add_tt_stage(score)


    def add_classic_time(self, time):
        self.boards_completed += 1
        time = int(time[0:2]) * 60 + int(time[3:5])
        with open(f"ms_user_data/Classic/{self.username}_Classic.txt", "a") as file:
            file.write(f"{time}\n")
        self.update_games_losses_boards()


    def add_tt_stage(self, stage, mine_clicked):
        with open(f"ms_user_data/Time Trial/{self.username}_Classic.txt", "a") as file:
            file.write(f"{stage}\n")

        #updating no. of boards completed and, POSSIBLY, no. of losses
        if mine_clicked:
            self.no_of_losses+=1
        self.update_games_losses_boards()


    def update_games_losses_boards(self):
        settings_file = open(f"ms_user_data/Settings/{self.username}_Settings.txt")
        settings_data = settings_file.readlines()
        settings_data[2] = f"{self.no_of_games},{self.no_of_losses},{self.boards_completed}\n"
        with open(f"ms_user_data/Settings/{self.username}_Settings.txt", "w") as file:
            for line in settings_data:
                file.write(line)


    def check_if_top_10_time(self, time):
        original_top_10 = self.top_10_classic
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


    #running out of time in time trial should not count as a loss, but hitting a mine in time trial should
    #def add_classic_loss(self):
    #    self.no_of_losses+=1
    #    settings_file = open(f"ms_user_data/settings/{self.username}_Settings.txt")
    #    settings_data = settings_file.readlines()
    #    settings_data[2] = f"{self.no_of_games},{self.no_of_losses},{self.boards_completed}\n"
    #    with open(f"ms_user_data/settings/{self.username}_Settings.txt", "w") as file:
    #        for line in settings_data:
    #            file.write(line)
