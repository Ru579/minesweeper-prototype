import os
from Settings import Settings

class DatabaseHandler:
    def __init__(self):
        # status attributes
        self.user_signed_in = False

        # profile information
        self.username = ""
        self.pword = ""
        
        # player data
        self.user_file_data = {}
        self.glb = {} #glb = games_losses_boards = no of games played, no of losses, no of boards completed (games won/ boards done in time trial)
        #each value in self.glb is a list, with the three values in the comment above. Each game-mode/difficulty has its own value in the dictionary
        self.average_scores = {}
        self.game_time = {}
        self.nonAver_games = {}
        # player ranking data
        self.top_10_scores = {}
        self.top_10_rank = 0
        self.no_1_status = ""
        # player EXP
        self.exp = 0
        self.level = 0

        # temporary sign in information- used during login
        self.temp_username = ""
        self.temp_pword = ""

        # other attributes
        self.difficulties = ["Beginner", "Intermediate", "Expert"] # for easy iteration through Classic mode difficulties

        # Loading data for currently logged-in player, otherwise loading guest data
        with open("ms_user_data/current_user_data.txt", "r") as current_user_file:
            username_line = current_user_file.readline()
            if username_line:
                self.username = str(username_line.strip("\n"))
                self.user_signed_in = True
                self.settings = Settings(self.username, user_signed_in=True)
                self.load_current_user_game_data()
            else:
                self.settings = Settings(self.username, user_signed_in=False)
                self.user_signed_in = False
        current_user_file.close()

        # TEXT FILE LAYOUT
        # GAME FILE: top 10 scores, GLB, average score, total game time, nonAver games, list of averaged scores, list of exact scores
        # SETTINGS FILE: password, profile picture colour, player level, player EXP, list of settings and their current value


    def find_user_file(self, username_input):
        directory = "ms_user_data/Settings"
        # iterating through all files until the user's file is found
        for file in os.listdir(directory):
            if str(file).lower() == f"{username_input.lower()}_settings.txt": # settings has a simple 's' because the file name has been .lower()-ed
                username_input = str(file)[0:len(str(file))-13] # extracting the exact case sensitive username from the file name
                self.temp_username = username_input
                
                # opening the user's settings file and extracting the password
                settings_file = open(f"ms_user_data/Settings/{username_input}_Settings.txt")
                settings_data = settings_file.readlines()
                settings_file.close()
                self.temp_pword = settings_data[0].strip("\n")

                return True # user's file has been found
        return False # user's file was not found
    
    def username_exists_check(self, username: str):
        # returns True if a file with the input username already exists
        directory = "ms_user_data/Settings"
        for file in os.listdir(directory):
            if str(file).lower()[0:len(str(file))-13] == username.lower():
                return True
        return False
    
    def check_pword(self, pword_input):
        if str(self.temp_pword) == pword_input:
            return True
        return False
    
    def sign_in_user(self):
        self.username = self.temp_username
        self.pword = self.temp_pword
        self.user_signed_in = True

        # writing to a file what player is currently signed in
        with open("ms_user_data/current_user_data.txt", "w") as file:
            file.write(f"{self.username}\n")
        file.close()

        # loading the player's scores
        self.load_current_user_game_data()
    
    def load_current_user_game_data(self):
        # loading the player's level, EXP, and settings
        with open(f"ms_user_data/Settings/{self.username}_Settings.txt") as settings_file:
            settings_data = settings_file.readlines()
            self.level = int(settings_data[2])
            self.exp = int(settings_data[3])
            # loading the user's settings
            self.settings.settings_user_sign_in(self.username, settings_data, exp=self.exp, level=self.level)
        settings_file.close()

        # loading all game data from files into attributes
        # opening classic data
        for difficulty in self.difficulties:
            with open(f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt") as classic_file:
                self.user_file_data[f"Cl{difficulty}"] = classic_file.readlines()
                self.load_file_data(f"Cl{difficulty}")
            classic_file.close()

        # opening time trial data
        with open(f"ms_user_data/Time Trial/{self.username}_Time Trial.txt") as tt_file:
            self.user_file_data["Time Trial"] = tt_file.readlines()
            self.load_file_data("Time Trial")
        tt_file.close()

    def load_file_data(self, specific_game_mode):
        # extracting top 10 scores from file
        top_10_scores_file_line = self.user_file_data[specific_game_mode][0].strip("\n") # extracting the top line from the text file- the top 10 scores
        top_10_scores_file_line = top_10_scores_file_line[1:len(top_10_scores_file_line)-1] # removing the square brackets from either side of the line
        self.top_10_scores[specific_game_mode] = top_10_scores_file_line.split(",") # splitting the line into individual scores and storing them in a list
        # turning each value in the list into an integer
        for i in range(10): 
            self.top_10_scores[specific_game_mode][i] = int(self.top_10_scores[specific_game_mode][i])
        # removing any bugged extra scores
        while len(self.top_10_scores[specific_game_mode]) > 10:
            del self.top_10_scores[specific_game_mode][10] 
        
        # extractubg GLB from file
        glb_file_line = self.user_file_data[specific_game_mode][1].strip("\n") # extracting the second line from the text file- the GLB list
        glb_file_line = glb_file_line[1:len(glb_file_line)-1] # removing square brackets
        self.glb[specific_game_mode] = glb_file_line.split(",") # splitting line into individual scores
        for i in range(3):
            self.glb[specific_game_mode][i] = int(self.glb[specific_game_mode][i])
        
        # extracting all-time average score from 3rd line of file
        self.average_scores[specific_game_mode] = int(self.user_file_data[specific_game_mode][2].strip("\n"))
        
        # extracting total game time from 4th line of file
        self.game_time[specific_game_mode] = int(self.user_file_data[specific_game_mode][3].strip("\n"))
        
        # extracting the number of games that haven't been averaged from the 5th line of file
        self.nonAver_games[specific_game_mode] = int(self.user_file_data[specific_game_mode][4].strip("\n"))

    def create_account(self, username, pword):
        self.settings.create_settings(username, pword)

        # creating new Time Trial text file
        with open(f"ms_user_data/Time Trial/{username}_Time Trial.txt", "w") as tt_file:
            tt_file.write("[0,0,0,0,0,0,0,0,0,0]\n[0,0,0]\n0\n0\n0\n&&&\n***\n")
        tt_file.close()

        # creating new Classic mode text file for each of the three difficulties
        for difficulty in self.difficulties:
            with open(f"ms_user_data/Classic/{difficulty}/{username}_Cl{difficulty}.txt", "w") as classic_file:
                classic_file.write("[999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999]\n[0,0,0]\n0\n0\n0\n&&&\n***\n")
                # incredibly high values equal to about 11.6 days are placeholders to make the list the correct length- will be passed over by Stats Menu
            classic_file.close()

        self.temp_username = username # sign_in_user() will then copy the value of self.temp_username to self.username
        self.sign_in_user()
    
    def delete_current_user(self):
        # deleting all of the player's files
        os.remove(f"ms_user_data/Settings/{self.username}_Settings.txt")
        os.remove(f"ms_user_data/Time Trial/{self.username}_Time Trial.txt")
        for difficulty in self.difficulties:
            os.remove(f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt")

        open("ms_user_data/current_user_data.txt","w").close() # resetting the contents of current_user_data
        self.user_signed_in = False
    
    def user_sign_out(self):
        open("ms_user_data/current_user_data.txt", "w").close()
        self.user_signed_in = False
        self.settings.settings_user_sign_out()
    
    def add_classic_win(self, stopwatch_time, difficulty):
        if self.user_signed_in:
            self.update_average_score(stopwatch_time, f"Cl{difficulty}")
            self.glb[f"Cl{difficulty}"][0] += 1 # increasing number of games played
            self.glb[f"Cl{difficulty}"][2] += 1 # increasing number of boards completed
            self.game_time[f"Cl{difficulty}"] += stopwatch_time

            self.update_top_10("Classic", stopwatch_time, difficulty)
            self.update_user_files("Classic", stopwatch_time, difficulty)
    
    def add_classic_loss(self, stopwatch_time, difficulty):
        if self.user_signed_in:
            self.glb[f"Cl{difficulty}"][0] += 1 # increasing number of games played
            self.glb[f"Cl{difficulty}"][1] += 1 # incrementing number of losses
            self.game_time[f"Cl{difficulty}"] += stopwatch_time
            self.update_user_files("Classic", difficulty=difficulty)
    
    def add_tt_stage(self, boards_completed, mine_clicked, stopwatch_time):
        if self.user_signed_in:
            self.update_average_score(boards_completed, "Time Trial")
            self.glb["Time Trial"][0] += 1 # incrementing number of games
            if mine_clicked:
                self.glb["Time Trial"][1] += 1 # incrementing number of losses only if a mine is revealed
            self.glb["Time Trial"][2] += boards_completed
            self.game_time["Time Trial"] += stopwatch_time

            self.update_top_10("Time Trial", boards_completed)
            self.update_user_files("Time Trial", boards_completed)
    
    def update_average_score(self, new_score, specific_game_mode):
        no_of_games = self.glb[specific_game_mode][0]
        no_of_losses = self.glb[specific_game_mode][1]
        # calculating the new average score
        # multiplying the current average by the number of scores added to the file (number of wins for Classic or number of games for Time Trial)
        self.average_scores[specific_game_mode] *= no_of_games if specific_game_mode == "Time Trial" else (no_of_games - no_of_losses)
        self.average_scores[specific_game_mode] += new_score
        # dividing new total by number of games in Time Trial or number of wins in Classic
        self.average_scores[specific_game_mode] /= (no_of_games + 1) if specific_game_mode == "Time Trial" else (no_of_games - no_of_losses + 1)
        self.average_scores[specific_game_mode] = round(self.average_scores[specific_game_mode])
    
    def update_top_10(self, game_mode, score, difficulty=""):
        specific_game_mode = f"Cl{difficulty}" if game_mode=="Classic" else "Time Trial"

        for i in range(9, -1, -1):
            if (
                (score >= self.top_10_scores[specific_game_mode][i] and game_mode=="Classic") or 
                (score <= self.top_10_scores[specific_game_mode][i] and game_mode=="Time Trial")
            ): # if achieved a worse or equal score
                self.top_10_scores[specific_game_mode].insert(i+1, score)
                del self.top_10_scores[specific_game_mode][10]

                self.top_10_rank = i+2 # +2 because we insert after the current index AND ranks start at 1, not 0
                break

            elif i==0:
                self.top_10_scores[specific_game_mode].insert(0, score)
                self.top_10_rank = 1
                self.no_1_status = "Reached"
        
        # determining if player has tied with top score
        if score == self.top_10_scores[specific_game_mode][0] == self.top_10_scores[specific_game_mode][1]:
            self.no_1_status = "Tied"
        
    def update_user_files(self, game_mode, score=None, difficulty=""):
        # setting up specific path to correct folder depending on game mode
        path=""
        specific_game_mode = ""
        if game_mode == "Classic":
            path=f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt"
            specific_game_mode = f"Cl{difficulty}"
        elif game_mode == "Time Trial":
            path = f"ms_user_data/Time Trial/{self.username}_Time Trial.txt"
            specific_game_mode = "Time Trial"
        
        # UPDATING ATTRIBUTES
        # if a score was passed in (ie. a loss in Classic DIDN'T occur), adds score to the end of the player's file
        if score is not None:
            self.user_file_data[specific_game_mode].append(f"{score}\n")
            self.nonAver_games[specific_game_mode] += 1

        # updating top_10_scores and glb of files
        self.user_file_data[specific_game_mode][0] = f"{self.top_10_scores[specific_game_mode]}\n"
        self.user_file_data[specific_game_mode][1] = f"{self.glb[specific_game_mode]}\n"
        self.user_file_data[specific_game_mode][2] = f"{self.average_scores[specific_game_mode]}\n"
        self.user_file_data[specific_game_mode][3] = f"{self.game_time[specific_game_mode]}\n"

        self.calc_100_average(specific_game_mode)
        # updating nonAver_games after calc_100_average possibly changed it
        self.user_file_data[specific_game_mode][4] = f"{self.nonAver_games[specific_game_mode]}\n"


        # WRITING TO FILE
        with open(path, "w") as rewrite_file:
            # writing player's new data to file
            for line in self.user_file_data[specific_game_mode]:
                rewrite_file.write(line)
        rewrite_file.close()
    
    def calc_100_average(self, specific_game_mode):        
        # averages the latest 100 game scores
        if self.nonAver_games[specific_game_mode] >= 100:
            total_score = 0
            bottom_entry_index = len(self.user_file_data[specific_game_mode]) - 1
            
            # starting from bottom of file, adding the score to a total and then deleting that line until *** marker is reached
            while self.user_file_data[specific_game_mode][bottom_entry_index] != "***\n":
                total_score += int(self.user_file_data[specific_game_mode][bottom_entry_index].strip("\n"))
                del self.user_file_data[specific_game_mode][bottom_entry_index] # accessing the attribute directly for deletion
                bottom_entry_index -= 1
            
            # adding the average score (total/100) to the line before the *** line (in the averages section)
            self.user_file_data[specific_game_mode].insert(len(self.user_file_data[specific_game_mode])-1, f"{round(total_score/100)}\n")

            # resets the number of games that haven't been averaged
            self.nonAver_games[specific_game_mode] = 0

