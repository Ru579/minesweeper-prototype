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
        self.top_10_rank = 100
        self.no_1_status = ""

        self.temp_username = ""
        self.temp_profile_pic_colour = ""
        self.temp_pword = ""

        #Loads in currently logged-in user, if there is one
        self.current_user_file = open("ms_user_data/current_user_data.txt")
        lines = self.current_user_file.readlines()
        if lines:
            self.username = str(lines[0].strip("\n"))
            self.profile_pic_colour = str(lines[1].strip("\n"))
            self.user_signed_in = True
            self.load_current_user_game_data()
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
        self.user_signed_in = True
        with open("ms_user_data/current_user_data.txt", "w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")
        self.load_current_user_game_data()


    def load_current_user_game_data(self):
        #opening classic data
        for difficulty in self.difficulties:
            with open(f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt") as classic_file:
                classic_data = classic_file.readlines()

                self.top_10_scores[f"Cl{difficulty}"] = classic_data[0].strip("\n")[1:len(classic_data[0])-2].split(",")
                for i in range(11): #because of the first value being the extra, extreme value
                    self.top_10_scores[f"Cl{difficulty}"][i] = int(self.top_10_scores[f"Cl{difficulty}"][i])

                self.glb[f"Cl{difficulty}"] = classic_data[1].strip("\n")[1:len(classic_data[1])-2].split(",")
                for i in range(3):
                    #print(self.glb[f"Cl{difficulty}"][i])
                    #print(self.glb)
                    self.glb[f"Cl{difficulty}"][i] = int(self.glb[f"Cl{difficulty}"][i])

        # opening time trial data
        with open(f"ms_user_data/Time Trial/{self.username}_Time Trial.txt") as tt_file:
            tt_data = tt_file.readlines()
            self.top_10_scores["Time Trial"] = tt_data[0].strip("\n")[1:len(tt_data[0])-2].split(",")
            for i in range(11): #because of the first value being the extra, extreme value
                self.top_10_scores["Time Trial"][i] = int(self.top_10_scores["Time Trial"][i])
            self.glb["Time Trial"] = tt_data[1].strip("\n")[1:len(tt_data[1])-2].split(",")
            for i in range(3):
                self.glb["Time Trial"][i] = int(self.glb["Time Trial"][i])


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
            file.write("[99999,0,0,0,0,0,0,0,0,0,0]\n[0,0,0]\n")#first number is very high so that top_10_stage checker will never have to deal with the very first index

        for difficulty in self.difficulties:
            with open(f"ms_user_data/Classic/{difficulty}/{username}_Cl{difficulty}.txt","w") as file:
                file.write("[-100,999999,999999,999999,999999,999999,999999,999999,999999,999999,999999]\n[0,0,0]\n")
                #first number is very low so that top_10_stage checker will never have to deal with the very first index, following numbers are very large so that user's time is guaranteed to be faster at first

        # Cl is put before the difficulty to signify that this is a classic game mode- just in case, in the future, other game modes are introduced that use game modes

        self.temp_username = username #set as temp_username because, in self.sign_in(), self.username = self.temp_username
        self.temp_profile_pic_colour = "red" #set as temp_profile_pic_colour for the same reasons as above
        self.sign_in_user()


    def change_profile_pic_colour(self, colour):
        self.profile_pic_colour = colour
        with open("ms_user_data/current_user_data.txt","w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")


    def add_classic_time(self, time, difficulty):
        self.glb[f"Cl{difficulty}"][2] += 1
        time = int(time[0:2]) * 60 + int(time[3:5])
        with open(f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt", "a") as file:
            file.write(f"{time}\n")
        self.check_if_top_10_time(time, difficulty)
        self.update_top_10_and_glb("Classic", difficulty)


    def add_tt_stage(self, stage, mine_clicked):
        with open(f"ms_user_data/Time Trial/{self.username}_Classic.txt", "a") as file:
            file.write(f"{stage}\n")

        #updating no. of boards completed and, POSSIBLY, no. of losses
        if mine_clicked:
            self.glb["Time Trial"][1] += 1

        self.check_if_top_10_stage(stage)
        self.update_top_10_and_glb("Time Trial")


    def update_top_10_and_glb(self, game_mode, difficulty=""):
        path=""
        specific_game_mode=""
        if game_mode=="Classic":
            path = f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt"
            specific_game_mode = f"Cl{difficulty}"
        elif game_mode=="Time Trial":
            path = f"ms_user_data/Time Trial/{self.username}_Time Trial.txt"
            specific_game_mode = "Time Trial"

        with open(path) as read_file:
            file_data = read_file.readlines()
            file_data[0] = f"{self.top_10_scores[specific_game_mode]}\n"
            #file_data[1] = f"{self.glb[specific_game_mode][0]},{self.glb[specific_game_mode][1]},{self.glb[specific_game_mode][2]}\n"
            file_data[1] = f"{self.glb[specific_game_mode]}\n"
        with open(path,"w") as rewrite_file:
            for line in file_data:
                rewrite_file.write(line)


    def check_if_top_10_time(self, time, difficulty): #for classic mode
        for i in range(10,-1,-1):
            #if not time<self.top_10_scores[f"Cl{difficulty}"][i]:
            if time>=self.top_10_scores[f"Cl{difficulty}"][i]:
                if i!=10:
                    self.top_10_scores[f"Cl{difficulty}"].insert(i + 1, time)
                    del self.top_10_scores[f"Cl{difficulty}"][11]
                    self.top_10_rank = i
                    if i==0:
                        self.no_1_status = "Reached"
                    elif time==self.top_10_scores[f"Cl{difficulty}"][1]:
                        self.no_1_status = "Tied"
                        #if self.top_10_scores[f"Cl{difficulty}"][i]==self.top_10_scores[f"Cl{difficulty}"][i+1]:
                        #    self.no_1_status="Tied" #player tied with their best time
                        #else:
                        #    self.no_1_status = "Reached" #player achieved a new best time

                break



    def check_if_top_10_stage(self, stage): #for time trial mode
        for i in range(10,-1,-1):
            if stage<=self.top_10_scores["Time Trial"][i]:
                if i!=10:
                    self.top_10_scores["Time Trial"].insert(i+1, stage)
                    del self.top_10_scores["Time Trial"][11]
                    self.top_10_rank = i
                    if i==0:
                        self.no_1_status = "Reached"
                    elif stage==self.top_10_scores["Time Trial"][1]:
                        self.no_1_status = "Tied"
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
