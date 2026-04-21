import os

class DatabaseHandler:
    def __init__(self):
        self.settings = None # settings object will be passed into this class by the GameManager

        # status attributes
        self.user_signed_in = False

        # profile information
        self.username = ""
        self.pword = ""
        
        # player data
        self.user_file_data = {}
        self.glb = {} #glb = games_losses_boards = no of games played, no of losses, no of boards completed (games won/ boards done in time trial)
        #each value in self.glb is a list, with the three values in the comment above. Each game-mode/difficulty has its own value in the dictionary
        self.game_time = {}
        self.nonAver_games = {}
        # player ranking data
        self.top_10_scores = {}
        self.top_10_rank = 100
        self.no_1_status = ""
        

        # temporary sign in information- used during login
        self.temp_username = ""
        self.temp_pword = ""

        # other attributes
        self.difficulties = ["Beginner", "Intermediate", "Expert"] # for easy iteration through Classic mode difficulties

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
        # loading the user's settings
        self.settings_user_sign_in()

        # loading the player's scores
        self.load_current_user_game_data()
    
    def load_current_user_game_data(self):
        # loading all data from files into attributes
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

    def load_file_data(self, file_name):
        # EXTRACTING TOP 10 SCORES FROM FILE
        top_10_scores_file_line = self.user_file_data[file_name][0].strip("\n") # extracting the top line from the text file- the top 10 scores
        top_10_scores_file_line = top_10_scores_file_line[1:len(top_10_scores_file_line)-2] # removing the square brackets from either side of the line
        self.top_10_scores[file_name] = top_10_scores_file_line.split(",") # splitting the line into individual scores and storing them in a list
        # turning each value in the list into an integer
        for i in range(10): 
            self.top_10_scores[file_name][i] = int(self.top_10_scores[file_name][i])
        
        # EXTRACTING GLB FROM FILE
        glb_file_line = self.user_file_data[file_name][1].strip("\n") # extracting the second line from the text file- the GLB list
        glb_file_line = glb_file_line[1:len(glb_file_line)-1] # removing square brackets
        self.glb[file_name] = glb_file_line.split(",") # splitting line into individual scores
        for i in range(3):
            self.glb[file_name][i] = int(self.glb[file_name][i])
        
        # extracting total game time from 3rd line of file
        self.game_time[file_name] = int(self.user_file_data[file_name][2].strip("\n"))
        
        # extracting the number of games that haven't been averaged from the 3th line of file
        self.nonAver_games[file_name] = int(self.user_file_data[file_name][3].strip("\n"))

    def create_account(self, username, pword):
        self.create_settings_file()

        with open(f"ms_user_data/Time Trial/{username}_Time Trial.txt", "w") as tt_file:
            tt_file.write("[0,0,0,0,0,0,0,0,0,0]\n[0,0,0]\n0\n0\n&&&\n***\n")
        tt_file.close()

        for difficulty in self.difficulties:
            with open(f"ms_user_data/Classic/{difficulty}/{username}_Cl{difficulty}.txt", "w") as classic_file:
                classic_file.write("[999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999]\n[0,0,0]\n0\n0\n&&&\n***\n")
                # incredibly high values equal to about 11.6 days are placeholders to make the list the correct length- will be passed over by Stats Menu
            classic_file.close()

        self.temp_username = username # sign_in_user() will then copy the value of self.temp_username to self.username
        self.sign_in_user()
    
    def delete_user(self):
        # deleting all of the player's files
        os.remove(f"ms_user_data/Settings/{self.username}_Settings.txt")
        os.remove(f"ms_user_data/Time Trial/{self.username}_Time Trial.txt")
        os.remove(f"ms_user_data/Exact Scores/Time Trial/{self.username}_Time Trial_long_term.txt")
        for difficulty in self.difficulties:
            os.remove(f"ms_user_data/Classic/{difficulty}/{self.username}_Cl{difficulty}.txt")
            os.remove(f"ms_user_data/Exact Scores/Classic/{difficulty}/{self.username}_Cl{difficulty}_long_term.txt")

        open("ms_user_data/current_user_data.txt","w").close() # resetting the contents of current_user_data
        self.user_signed_in = False
    
    def user_sign_out(self):
        open("ms_user_data/current_user_data.txt", "w").close()
        self.user_signed_in = False
        self.settings_user_sign_out()
    
    def update_top_10(self, score, game_mode, difficulty=""):
        specific_game_mode = f"Cl{difficulty}" if game_mode=="Classic" else "Time Trial"

        for i in range(9, -1, -1):
            if (
                (score <= self.top_10_scores[specific_game_mode][i] and game_mode=="Classic") or 
                (score >= self.top_10_scores[specific_game_mode][i] and game_mode=="Time Trial")
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
        if score == self.top_10_scores[specific_game_mode][0]:
            self.no_1_status = "Tied"





    def settings_user_sign_in(self):
        pass

    def create_settings_file(self):
        pass

    def settings_user_sign_out(self):
        pass
