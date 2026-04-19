from Board import Board
from time import sleep
from DatabaseHandler import DatabaseHandler

class GameManager:
    def __init__(self):
        #initialising attributes
        self.board = Board(0,0,0)
        
        self.game_mode = ""
        self.board_started = False
        
        # game over attributes
        self.game_won = False
        self.mines_revealed = False

        self.user_can_interact = True

        # Classic mode attributes
        self.difficulty = ""
        self.main_menu_difficulty = "Beginner"
        self.difficulty_mapper = {
            "Beginner": "Intermediate",
            "Intermediate": "Expert", 
            "Expert": "Beginner"
        }
        self.loss_bonuses = {
            "Beginner": 30,
            "Intermediate": 100,
            "Expert": 300
        }

        # Time Trial attributes
        self.tt_running = False # becomes True when a game of TT starts- is used by the clock
        self.stage_length = 0 # corresponds to the length of one side of the square board
        self.previous_tt_difficulty = ""
        self.tt_difficulty = ""
        self.board_done = False # checks whether an individual board has been completed- is different to game_won since you can't win in Time Trial
        self.swapped_to_hard_tt = False # used for swapping to smaller cells on GUI
        
        # timer related attributes
        self.timer_on = False
        self.minutes = 0
        self.seconds = 0
        self.stopwatch = 0
        self.time_change_type = "" # used by GUI to determine what should happen based on state of timer (eg. has timer reached , meaning game over)
        self.time_to_be_added = False # used to determine when time needs to be added to the timer
        self.bonus_times = {
            "Easy": 30,
            "Medium": 45,
            "Hard": 60,
            "Very Hard": 90
        }

        # EXP related
        self.exp = 0
        
        # database handler attributes
        self.database = DatabaseHandler()
        
        
        self.top_10_rank = 0
        self.no_1_states = ""

    def start_classic_mode(self, difficulty: str):
        self.difficulty = difficulty
        self.game_mode = "Classic"
        self.tt_difficulty = "" # stopping other game mode difficulty from influencing cell size
        self.reset_starting_game_variables()

        #creating board
        if difficulty == "Beginner":
            self.board = Board(8, 8, 10)
        elif difficulty == "Intermediate":
            self.board = Board(16,16, 40)
        elif difficulty == "Expert":
            self.board = Board(16, 30, 99)
        else:
            raise ValueError("Invalid Classic Difficulty")
    
    def start_time_trial(self):
        # initialising game state variables
        self.game_mode = "Time Trial"
        self.tt_running = False # is set to True after the first click on a Time Trial board to coordinate with GUI timers
        self.difficulty = "" # stopping other game mode difficulty from influencing cell size
        self.reset_starting_game_variables()
        # the starting value of the timer
        self.minutes = 0
        self.seconds = 10

        self.stage_length = 6 # starting stage: first board has a length of 6
        self.tt_difficulty = "Easy"

        #creating the first board
        self.board = Board(self.stage_length, self.stage_length, self.calculate_mine_number())
    
    def calculate_mine_number(self):
        # returns the number of mines that should be on a square board of a specific length
        # floats determine mine concentration
        if self.tt_difficulty == "Easy":
            return round(0.13 * (self.stage_length ** 2))
        elif self.tt_difficulty == "Medium":
            return round(0.175 * (self.stage_length ** 2))
        elif self.tt_difficulty == "Hard":
            return round(0.206 * (self.stage_length ** 2))
        elif self.tt_difficulty == "Very Hard":
            return round(0.237 * (self.stage_length ** 2))
        else:
            raise ValueError("Invalid Time Trial Difficulty")
    
    def set_difficulty(self):
        # the first stage is stage 6, as stage = board length and the first board is a 6x6
        if self.stage_length < 10:
            self.tt_difficulty = "Easy"
        elif 10 <= self.stage_length <= 16:
            self.tt_difficulty = "Medium"
        elif 17 <= self.stage_length <= 23:
            self.tt_difficulty = "Hard"
        else:
            self.tt_difficulty = "Very Hard"
    
    def next_tt_stage(self):
        self.timer_on = False # stopping timer from running until the user first clicks on a cell on the new board
        self.time_to_be_added = True
        self.stage_length += 1
        
        # creating the next board after setting the difficulty (difficulty depends on stage reached)
        self.previous_tt_difficulty = self.tt_difficulty
        self.set_difficulty()
        self.board = Board(self.stage_length, self.stage_length, self.calculate_mine_number())

        # resetting whether the board has been completed since a new board has been created
        self.board_done = False

        if not self.swapped_to_hard_tt and self.tt_difficulty == "Hard":
            self.swapped_to_hard_tt = True
    
    def open_cell(self, x: int, y: int):
        self.board.open_cell(x, y, self.board_started)
        
        #starting the timer after the first click on the board
        if not self.board_started:
            self.timer_on = True
            # board_started is set to true in the GUI to coordinate with the starting of the timers
        
        self.board_done_check()
    
    
    def board_done_check(self):
        # if user has revealed all non-mine cells
        if self.board.revealed_cells == self.board.grid_height * self.board.grid_width - self.board.no_of_mines and not self.board.game_over:
            if self.game_mode == "Classic":
                self.game_won = True
            elif self.game_mode == "Time Trial":
                self.board_done = True
            else:
                raise ValueError("Invalid Game Mode")
            self.user_can_interact = False
    
    def update_countdown_timer(self):
        # resetting time_change_type from last countdown timer update
        self.time_change_type = ""

        if self.timer_on:
            self.stopwatch += 1
            # decrementing timer by 1 second
            self.seconds -= 1
            if self.seconds < 0:
                self.seconds = 59
                self.minutes -= 1
            if self.seconds == 0 and self.minutes == 0:
                self.board.game_over = True
                self.time_change_type = "Time Game Over"
            else:
                self.time_change_type = "Time Normal"
        else:
            if self.time_to_be_added:
                # adding time to the timer
                total_time = self.minutes * 60 + self.seconds
                total_time += self.bonus_times[self.previous_tt_difficulty] # adding time based on the difficulty of the stage JUST completed
                self.time_to_be_added = False
                # restoring total time to minutes:seconds format
                self.minutes = total_time // 60
                self.seconds = total_time % 60
                self.time_change_type = "Time Added"
    
    def add_exp(self, final_score: int, outcome = ""):
        # final score is the time taken for Classic mode or the stage reached in Time Trial
        # for Time Trial, stage reached = final_score = stage_length - 5
        exp_to_add = 0
        if self.game_mode == "Classic":
            # adding EXP based on the difficulty of the board and the score achieved by the player
            if self.difficulty == "Beginner":
                exp_to_add = self.add_classic_mode_exp(outcome, final_score, base_exp=200, max_bonus=100)
            elif self.difficulty == "Intermediate":
                exp_to_add = self.add_classic_mode_exp(outcome, final_score, base_exp=600, max_bonus=200)
            elif self.difficulty == "Expert":
                exp_to_add = self.add_classic_mode_exp(outcome, final_score, base_exp=1000, max_bonus=350)
            else:
                raise ValueError("Invalid Classic Difficulty")
            
            # adding EXP if the player achieves a new best score/ top 10 score
            if outcome == "Win":
                exp_to_add += self.add_personal_best_exp()
        
        elif self.game_mode == "Time Trial":
            if final_score == 1:
                # adding exp based on the fraction of the board that was revealed and the difficulty of that board
                exp_to_add = round(30 * self.board.revealed_cells / (self.board.grid_height * self.board.grid_width))
                print(exp_to_add)
            elif final_score > 1:
                exp_to_add = 38 * (final_score**2) - 90 * (final_score) + 100 # the quadratic equation used for calculating Time Trial EXP
                if self.swapped_to_hard_tt:
                    exp_to_add *= 1.2
                    exp_to_add = round(exp_to_add)
                exp_to_add += self.add_personal_best_exp()
            else:
                raise ValueError("Final score can't be less than 1.")
        else:
            raise ValueError("Invalid Game Mode")
        self.exp += exp_to_add


    def add_classic_mode_exp(self, outcome:str, final_score:int , base_exp: int, max_bonus: int):
        # base_exp is the minimum EXP earnt when completing a Classic board.
        # max_bonus is the maximum amount of additional EXP that the player can earn depending on how quickly they completed the board
        if outcome == "Win":
            # adding a portion of the max_bonus depending on how good the final_score is
            if final_score <= max_bonus:
                return base_exp + (max_bonus - final_score)
            else:
                return base_exp
        elif outcome == "Lose":
            loss_bonus = self.loss_bonuses[self.difficulty]
            # adding exp based on the fraction of the board that was revealed and the difficulty of that board
            return round(loss_bonus * (self.board.revealed_cells / (self.board.grid_height * self.board.grid_width)))
    
    def add_personal_best_exp(self):
        return 0
        #exp_to_add = 0
        #if self.top_10_rank:
        #    exp_to_add += 200
        #    if self.no_1_status == "Tied":
        #        exp_to_add += 200
        #    elif self.no_1_status == "Reached":
        #        exp_to_add += 500
        #return exp_to_add
    
    def get_cell(self, x, y, info_needed):
        # returns information about a cell
        if info_needed=="value":
            return self.board.grid[x][y].value
        elif info_needed == "state":
            return self.board.grid[x][y].state
    
    def terminate_game_variables(self):
        self.timer_on = False
        self.board_started = False
        self.user_can_interact = False

    def reset_starting_game_variables(self):
        self.board_started = False
        self.board_done = False
        self.game_won = False
        self.mines_revealed = False
        self.outcome = ""
        self.swapped_to_hard_tt = False
        self.stopwatch = 0

    def calculate_output_statement(self):
        # calculating how long the player took
        final_time = [f"{self.stopwatch // 60:02}", f"{self.stopwatch % 60:02}"]
        return("YOUR TIME HERE")

