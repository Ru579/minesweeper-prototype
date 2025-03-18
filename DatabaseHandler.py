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
        self.difficulties = ["Beginner", "Intermediate", "Expert"]
        #glb = games_losses_boards = no of games played, no of losses, no of boards completed (games won/ boards done in time trial)
        self.glb = {}
        #each value in self.glb is a list, with the three values in the comment above. Each game-mode/difficulty has its own value in the dictionary
        self.top_10_scores = {}

        self.temp_username = ""
        self.temp_profile_pic_colour = ""
        self.temp_pword = ""
        #self.temp_no_of_games = 0
        #self.temp_no_of_losses = 0
        #self.temp_boards_completed = 0

        #self.top_10_classic = []
        #self.top_10_time_trial = []

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


    #def sign_in_user(self):
    #    self.username = self.temp_username
    #    self.pword = self.temp_pword
    #    self.profile_pic_colour = self.temp_profile_pic_colour
    #    #with open(f"ms_user_data/Settings/{self.username}_Settings.txt") as file:
    #    #    settings_data = file.readlines()
    #    #    games_losses_boards = settings_data[2].strip("\n").split(",")
    #    #self.no_of_games = int(games_losses_boards[0])
    #    #self.no_of_losses = int(games_losses_boards[1])
    #    #self.boards_completed = int(games_losses_boards[2])
    #    self.user_signed_in = True
    #    with open("ms_user_data/current_user_data.txt", "w") as file:
    #        file.write(f"{self.username}\n{self.profile_pic_colour}\n")
    #    with open(f"ms_user_data/Classic/{self.username}_Classic.txt") as classic_file:
    #        data = classic_file.readlines()
    #        self.top_10_classic = data[0].split(",")
    #    with open(f"ms_user_data/Time Trial/{self.username}_Time Trial.txt") as tt_file:
    #        data = tt_file.readlines()
    #        self.top_10_time_trial = data[0].split(",")
    #    #converting arrays values from strings into integers
    #    for i in range(10):
    #        self.top_10_classic[i] = int(self.top_10_classic[i])
    #        self.top_10_time_trial[i] = int(self.top_10_time_trial[i])


    def sign_in_user(self):
        self.username = self.temp_username
        self.pword = self.temp_pword
        self.profile_pic_colour = self.temp_profile_pic_colour
        self.user_signed_in = True
        with open("ms_user_data/current_user_data.txt", "w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")

        #opening classic data
        for difficulty in self.difficulties:
            with open(f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt") as classic_file:
                classic_data = classic_file.readlines()
                self.top_10_scores[f"Cl{difficulty}"] = classic_data[0].strip("\n").split(",")
                for i in range(10):
                    self.top_10_scores[f"Cl{difficulty}"][i] = int(self.top_10_scores[f"Cl{difficulty}"][i])
                self.glb[f"Cl{difficulty}"] = classic_data[1].strip("\n").split(",")


        # opening time trial data
        with open(f"ms_user_data/Time Trial/{self.username}_Time Trial.txt") as tt_file:
            tt_data = tt_file.readlines()
            self.top_10_scores["Time Trial"] = tt_data[0].strip("\n").split(",")
            self.glb["Time Trial"] = tt_data[1].strip("\n").split(",")
            for i in range(10):
                self.top_10_scores["Time Trial"][i] = int(self.top_10_scores["Time Trial"][i])


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
        with open(f"ms_user_data/Settings/{username}_Settings.txt", "w") as file:
            file.write(f"{pword}\nred\n")

        with open(f"ms_user_data/Time Trial/{username}_Time Trial.txt","w") as file:
            file.write("0,0,0,0,0,0,0,0,0,0\n0,0,0\n")

        for difficulty in self.difficulties:
            with open(f"ms_user_data/Classic/{difficulty}/{username}_ClBeginner.txt","w") as file:
                file.write("0,0,0,0,0,0,0,0,0,0\n0,0,0\n")
        # Cl is put before the difficulty to signify that this is a classic game mode- just in case, in the future, other game modes are introduced that use game modes

        self.temp_username = username #set as temp_username because, in self.sign_in(), self.username = self.temp_username
        self.temp_profile_pic_colour = "red" #set as temp_profile_pic_colour for the same reasons as above
        self.sign_in_user()


    def change_profile_pic_colour(self, colour):
        self.profile_pic_colour = colour
        with open("ms_user_data/current_user_data.txt","w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")


    def add_classic_time(self, time, difficulty):
        #self.boards_completed += 1
        #time = int(time[0:2]) * 60 + int(time[3:5])
        #with open(f"ms_user_data/Classic/{self.username}_Classic.txt", "a") as file:
        #    file.write(f"{time}\n")
        #self.update_top_10_and_glb()
        self.glb[difficulty][2] += 1
        time = int(time[0:2]) * 60 + int(time[3:5])
        with open(f"ms_user_data/Classic/{self.username}_Classic.txt", "a") as file:
            file.write(f"{time}\n")
        self.update_top_10_and_glb("Classic", difficulty)


    def add_tt_stage(self, stage, mine_clicked):
        with open(f"ms_user_data/Time Trial/{self.username}_Classic.txt", "a") as file:
            file.write(f"{stage}\n")

        #updating no. of boards completed and, POSSIBLY, no. of losses
        #if mine_clicked:
        #    self.no_of_losses+=1
        #self.update_top_10_and_glb()
        if mine_clicked:
            self.glb["Time Trial"][1] += 1
        self.update_top_10_and_glb("Time Trial")


    #def update_top_10_and_glb(self):
    #    settings_file = open(f"ms_user_data/Settings/{self.username}_Settings.txt")
    #    settings_data = settings_file.readlines()
    #    settings_data[2] = f"{self.no_of_games},{self.no_of_losses},{self.boards_completed}\n"
    #    with open(f"ms_user_data/Settings/{self.username}_Settings.txt", "w") as file:
    #        for line in settings_data:
    #            file.write(line)

    def update_top_10_and_glb(self, game_mode, difficulty=""):
        #if game_mode=="Classic":
        #    with open(f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt") as read_cl_file:
        #        classic_data = read_cl_file.readlines()
        #        formatted_difficulty = f"Cl{difficulty}"
        #        classic_data[1] = f"{self.glb[formatted_difficulty][0]},{self.glb[formatted_difficulty][1]},{self.glb[formatted_difficulty][2]}\n"
        #    with open(f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt","w") as write_cl_file:
        #        for line in classic_data:
        #            write_cl_file.write(line)
        path=""
        specific_game_mode=""
        if game_mode=="Classic":
            path = f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt"
            specific_game_mode = f"Cl{difficulty}"
            rank = self.check_if_top_10_time()
        elif game_mode=="Time Trial":
            path = f"ms_user_data/Time Trial/{self.username}_Time Trial.txt"
            specific_game_mode = "Time Trial"

        with open(path) as read_file:
            file_data = read_file.readlines()
            file_data[1] = f"{self.glb[specific_game_mode][0]},{self.glb[specific_game_mode][1]},{self.glb[specific_game_mode][2]}\n"
        with open(path,"w") as rewrite_file:
            for line in file_data:
                rewrite_file.write(line)


    def check_if_top_10_time(self, time, difficulty): #for classic mode
        #original_top_10 = self.top_10_scores[f"Cl{difficulty}"]
        for i in range(0, 10, -1):
            if time>self.top_10_scores[f"Cl{difficulty}"][i]:
                if i!=9:
                    self.top_10_scores[f"Cl{difficulty}"].insert(i+1, time)
                    del self.top_10_scores[f"Cl{difficulty}"][10]
                    #break
                    return i
                return 100 #100 will be used to represent that the time was not in the top 10


    def check_if_top_10_stage(self, stage): #for time trial mode
        for i in range(0,10,-1):
            if stage<self.top_10_scores["Time Trial"][i]:
                if i!=9:
                    self.top_10_scores["Time Trial"].insert(i+1, stage)
                    del self.top_10_scores["Time Trial"][10]
                    #break
                    return i
                return 100  # 100 will be used to represent that the time was not in the top 10


    #running out of time in time trial should not count as a loss, but hitting a mine in time trial should
    #def add_classic_loss(self):
    #    self.no_of_losses+=1
    #    settings_file = open(f"ms_user_data/settings/{self.username}_Settings.txt")
    #    settings_data = settings_file.readlines()
    #    settings_data[2] = f"{self.no_of_games},{self.no_of_losses},{self.boards_completed}\n"
    #    with open(f"ms_user_data/settings/{self.username}_Settings.txt", "w") as file:
    #        for line in settings_data:
    #            file.write(line)
