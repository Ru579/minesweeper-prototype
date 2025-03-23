import os
import datetime

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

        #The number of games ina file that haven't been averaged
        self.nonAver_games = {}

        self.temp_username = ""
        self.temp_profile_pic_colour = ""
        self.temp_pword = ""

        self.user_file_data = {}

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
            #if str(file).lower() == f"{username.lower()}_Settings.txt":
            if f"{str(file).lower()[0:len(str(file)) - 13]}_Settings.txt" == f"{username.lower()}_Settings.txt":
                username = str(file)[0:len(str(file))-13]
                self.temp_username = username
                settings_file = open(f"ms_user_data/Settings/{username}_Settings.txt")

                settings_data = settings_file.readlines()
                self.temp_pword = settings_data[0].strip("\n")
                self.temp_profile_pic_colour = settings_data[1].strip("\n")

                return True
        return False


    def check_pword(self, password):
        if str(self.temp_pword) == password:
            return True
        return False


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
                self.user_file_data[f"Cl{difficulty}"] = classic_file.readlines()

                self.top_10_scores[f"Cl{difficulty}"] = self.user_file_data[f"Cl{difficulty}"][0].strip("\n")[1:len(self.user_file_data[f"Cl{difficulty}"][0])-2].split(",")
                for i in range(11): #because of the first value being the extra, extreme value
                    self.top_10_scores[f"Cl{difficulty}"][i] = int(self.top_10_scores[f"Cl{difficulty}"][i])

                self.glb[f"Cl{difficulty}"] = self.user_file_data[f"Cl{difficulty}"][1].strip("\n")[1:len(self.user_file_data[f"Cl{difficulty}"][1])-2].split(",")
                for i in range(3):
                    self.glb[f"Cl{difficulty}"][i] = int(self.glb[f"Cl{difficulty}"][i])

                self.nonAver_games[f"Cl{difficulty}"] = int(self.user_file_data[f"Cl{difficulty}"][2].strip("\n"))


        # opening time trial data
        with open(f"ms_user_data/Time Trial/{self.username}_Time Trial.txt") as tt_file:
            self.user_file_data["Time Trial"] = tt_file.readlines()

            self.top_10_scores["Time Trial"] = self.user_file_data["Time Trial"][0].strip("\n")[1:len(self.user_file_data["Time Trial"][0])-2].split(",")
            for i in range(11): #because of the first value being the extra, extreme value
                self.top_10_scores["Time Trial"][i] = int(self.top_10_scores["Time Trial"][i])

            self.glb["Time Trial"] = self.user_file_data["Time Trial"][1].strip("\n")[1:len(self.user_file_data["Time Trial"][1])-2].split(",")
            for i in range(3):
                self.glb["Time Trial"][i] = int(self.glb["Time Trial"][i])

            self.nonAver_games["Time Trial"] = int(self.user_file_data["Time Trial"][2].strip("\n"))


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
            if f"{str(file).lower()[0:len(str(file))-13]}_Settings.txt"==f"{username.lower()}_Settings.txt":
                return True
        return False


    def create_account(self, username, pword):
        with open(f"ms_user_data/Settings/{username}_Settings.txt", "w") as file:
            file.write(f"{pword}\nred\n")

        with open(f"ms_user_data/Time Trial/{username}_Time Trial.txt","w") as file:
            file.write("[99999,0,0,0,0,0,0,0,0,0,0]\n[0,0,0]\n0\n&&&\n***\n")#first number is very high so that top_10_stage checker will never have to deal with the very first index
        open(f"ms_user_data/Exact Scores/Time Trial/{username}_Time Trial_long_term.txt", "w").close()

        for difficulty in self.difficulties:
            with open(f"ms_user_data/Classic/{difficulty}/{username}_Cl{difficulty}.txt","w") as file:
                file.write("[-100,999999,999999,999999,999999,999999,999999,999999,999999,999999,999999]\n[0,0,0]\n0\n&&&\n***\n")
                #first number is very low so that top_10_stage checker will never have to deal with the very first index, following numbers are very large so that user's time is guaranteed to be faster at first
            open(f"ms_user_data/Exact Scores/Classic/{difficulty}/{username}_Cl{difficulty}_long_term.txt","w") .close()

        # *** is used to separate average scores from the normal scores added to the file
        # &&& is used to separate average scores from the beginning three lines (top 10, glb, nonAver_games)

        # Cl is put before the difficulty to signify that this is a classic game mode- just in case, in the future, other game modes are introduced that use game modes

        self.temp_username = username #set as temp_username because, in self.sign_in(), self.username = self.temp_username
        self.temp_profile_pic_colour = "red" #set as temp_profile_pic_colour for the same reasons as above
        self.sign_in_user()


    def change_profile_pic_colour(self, colour):
        self.profile_pic_colour = colour
        with open("ms_user_data/current_user_data.txt","w") as file:
            file.write(f"{self.username}\n{self.profile_pic_colour}\n")


    def delete_user(self):
        os.remove(f"ms_user_data/Settings/{self.username}_Settings.txt")
        os.remove(f"ms_user_data/Time Trial/{self.username}_Time Trial.txt")
        os.remove(f"ms_user_data/Exact Scores/Time Trial/{self.username}_Time Trial_long_term.txt")
        for difficulty in self.difficulties:
            os.remove(f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt")
            os.remove(f"ms_user_data/Exact Scores/Classic/{difficulty}/{self.username}_Cl{difficulty}_long_term.txt")

        open("ms_user_data/current_user_data.txt","w").close()
        self.user_signed_in = False


    def add_classic_time(self, time, difficulty):
        time = int(time[0:2]) * 60 + int(time[3:5])

        # increasing the number of boards completed
        self.glb[f"Cl{difficulty}"][2] += 1
        # increasing the number of games that haven't been averaged
        self.nonAver_games[f"Cl{difficulty}"] += 1



        with open(f"ms_user_data/Exact Scores/Classic/{difficulty}/{self.username}_Cl{difficulty}_long_term.txt", "a") as file:
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            file.write(f"{time}:{date}\n")

        self.update_top_10(time, "Classic", difficulty)
        self.update_user_files("Classic", time, difficulty)


    def add_tt_stage(self, stage, mine_clicked):
        # updating no. of boards completed and, POSSIBLY, no. of losses
        if mine_clicked:
            self.glb["Time Trial"][1] += 1
        # increasing the number of games that haven't been averaged
        self.nonAver_games["Time Trial"] += 1


        with open(f"ms_user_data/Exact Scores/Time Trial/{self.username}_Time Trial_long_term.txt", "a") as file:
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            file.write(f"{stage}:{date}\n")

        self.update_top_10(stage, "Time Trial")
        self.update_user_files("Time Trial", stage)


    def add_classic_loss(self, difficulty):
        self.glb[f"Cl{difficulty}"][1] += 1
        self.update_user_files("Classic", difficulty=difficulty)


    def update_user_files(self, game_mode, score=None, difficulty=""):
        # setting up specific path to correct folder
        path = ""
        specific_game_mode = ""
        if game_mode == "Classic":
            path = f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt"
            specific_game_mode = f"Cl{difficulty}"
        elif game_mode == "Time Trial":
            path = f"ms_user_data/Time Trial/{self.username}_Time Trial.txt"
            specific_game_mode = "Time Trial"

        # updating top_10_scores and glb of files
        self.user_file_data[specific_game_mode][0] = f"{self.top_10_scores[specific_game_mode]}\n"
        self.user_file_data[specific_game_mode][1] = f"{self.glb[specific_game_mode]}\n"
        #self.user_file_data[specific_game_mode][2] = f"{self.nonAver_games[specific_game_mode]}\n"

        #adds the score to database's attribute of user_data if not just adding a loss
        if score is not None:
            self.user_file_data[specific_game_mode].append(f"{score}\n")


        with open(path, "w") as rewrite_file:
            self.calc_100_average(game_mode, difficulty)
            self.user_file_data[specific_game_mode][2] = f"{self.nonAver_games[specific_game_mode]}\n" #nonAver_games must be updated after calc_100 has possibly changed it
            for line in self.user_file_data[specific_game_mode]:
                rewrite_file.write(line)


    def update_top_10(self, score, game_mode, difficulty=""):
        specific_game_mode = f"Cl{difficulty}" if game_mode=="Classic" else "Time Trial"
        for i in range(10,-1,-1):
            if (score>=self.top_10_scores[specific_game_mode][i] and game_mode=="Classic") or (score<=self.top_10_scores[specific_game_mode][i] and game_mode=="Time Trial"):
                if i != 10:
                    self.top_10_scores[specific_game_mode].insert(i+1, score)
                    del self.top_10_scores[specific_game_mode][11]
                    #self.top_10_rank = i
                    self.top_10_rank = i + 1

                    if i==0:
                        self.no_1_status = "Reached"
                    elif score==self.top_10_scores[specific_game_mode][1]:
                        self.no_1_status = "Tied"
                break


    #must be called after the data has been added, otherwise, there is a chance that the program could be forcefully closed at the wrong time?
    #add to Minesweeper Progress how we thought about when we could call this function, since you we update glb when a game is started, but don't update the actual file until the game is done.

    #NEED TO CHOOSE between just reading what the number of games are from glb, or calculating the length of the file- the former is most likely faster/more efficient

    def calc_100_average(self, game_mode, difficulty):
        specific_game_mode = game_mode if game_mode=="Time Trial" else f"Cl{difficulty}"

        #if len(self.user_file_data[specific_game_mode])>101:
        if self.nonAver_games[specific_game_mode]>=100:
            # sums final 100 lines
            start_sum = False
            total = 0
            for line in self.user_file_data[specific_game_mode]:
                if line == "***\n":
                    start_sum = True
                elif start_sum:
                    i = len(self.user_file_data[specific_game_mode])-1
                    while self.user_file_data[specific_game_mode][i] != "***\n":
                        total += int(self.user_file_data[specific_game_mode][i].strip("\n"))
                        del self.user_file_data[specific_game_mode][i]
                        i -= 1
                    break
            total /= 100

            self.user_file_data[specific_game_mode].insert(len(self.user_file_data[specific_game_mode]) - 1, str(total)+"\n")

            # resets the number fo games that haven't been averaged
            self.nonAver_games[specific_game_mode] = 0




