from Board import *
from DatabaseHandler import *

#need to update this file to deal with the new glb array, not just no. of losses

class GameManager:
    def __init__(self):
        self.game_started = False
        self.board = Board()
        self.flag_difference = 0
        self.mines_left = 0
        self.mines_revealed = False
        self.difficulty = ""
        self.tt_difficulty = ""  # difficulty for time trial
        self.swapped_to_hard_tt = False
        self.game_has_been_won = False
        self.board_done = False
        self.game_mode = ""
        self.timer_on = False
        self.stopwatch = 0
        self.countdown_timer = ""
        self.stage = 0
        self.tt_running = False #used to determine when the timer should first start (upon first click on first board) and when it ends (tt game over)
        self.user_can_interact = False
        self.time_to_be_added = False
        self.time_change_type = ""
        self.bonus_times = {
            "Easy": 30,
            "Medium": 45,
            "Hard": 60,
            "Very Hard": 90
        }
        self.loginGUI = None
        self.freeplay_enabled = False
        self.top_10_rank = 100
        self.no_1_status = ""

        #TEMP
        self.database = DatabaseHandler()


    def start_classic_mode(self, difficulty):
        self.difficulty = difficulty
        self.game_mode = "Classic"
        self.game_has_been_won = False
        self.mines_revealed=False
        #self.database.no_of_games += 1
        if self.database.user_signed_in:
            self.database.glb[f"Cl{self.difficulty}"][0]+=1
        if difficulty == "Beginner":
            self.board = Board(8, 8, 10)
            self.mines_left = 10
        elif difficulty == "Intermediate":
            self.board = Board(16, 16, 40)
            self.mines_left = 40
        elif difficulty == "Expert":
            self.board = Board(16, 30, 99)
            self.mines_left = 99
        else:
            print("Not a proper difficulty given")#CHECKING LINE

    def start_time_trial(self):
        self.game_mode = "Time Trial"
        self.board_done = False
        self.game_has_been_won = False
        self.board.game_over = False
        self.mines_revealed = False
        self.swapped_to_hard_tt = False
        self.stage = 6
        self.stopwatch = 0
        self.tt_difficulty = "Easy"
        #self.database.no_of_games += 1
        if self.database.user_signed_in:
            self.database.glb["Time Trial"][0]+=1
        self.board = Board(self.stage, self.stage, self.board.calculate_no_of_mines(self.stage, "Easy"))
        self.mines_left = self.board.calculate_no_of_mines(self.stage, "Easy")

    def get_cell(self, x, y, info_needed):
        if info_needed == "value":
            return self.board.grid[x][y].value
        elif info_needed == "state":
            return self.board.grid[x][y].state

    def open_cell(self, x, y):
        self.board.open_cell(x, y, self.game_started)
        self.flag_difference = self.board.flag_difference
        self.board.flag_difference = 0
        if not self.game_started:
            self.game_has_been_won = False
            self.timer_on = True
        self.board_done_check()

    def flag_cell(self, x, y):
        self.board.flag_cell(x, y, self.mines_left)
        if self.board.grid[x][y].state == "Flagged":
            self.mines_left -= 1
        elif self.board.grid[x][y].state != "Revealed" and self.board.was_flagged == True:
            self.mines_left += 1
            self.board.was_flagged = False

    def confuse_cell(self, x, y):
        cell_was_flagged = False
        if self.board.grid[x][y].state == "Flagged":
            cell_was_flagged = True
        self.board.confuse_cell(x, y)
        if cell_was_flagged:
            self.mines_left += 1

    def board_done_check(self):
        if self.board.revealed_cells == self.board.grid_width * self.board.grid_height - self.board.no_of_mines and not self.board.game_over:
            if self.game_mode == "Classic":
                self.game_has_been_won = True
            elif self.game_mode == "Time Trial":
                self.board_done = True
            self.user_can_interact = False

    def update_countdown_timer(self, minutes, seconds):
        minutes = int(minutes)
        seconds = int(seconds)
        if self.timer_on:
            self.stopwatch += 1
            seconds -= 1
            if seconds < 0:
                seconds = 59
                minutes -= 1
            if seconds == 0 and minutes == 0:
                self.board.game_over = True
                self.time_change_type = "Time Game Over"
            else:
                self.time_change_type = "Time Normal"
        else:
            if self.time_to_be_added:
                total_time = minutes * 60 + seconds
                total_time += self.bonus_times[self.tt_difficulty]
                self.time_to_be_added = False
                minutes = total_time // 60
                seconds = total_time % 60
                self.time_change_type = "Time Added"
        return minutes, seconds

    def next_tt_stage(self):
        self.timer_on = False
        self.stage += 1
        #self.database.boards_completed += 1
        if self.database.user_signed_in:
            self.database.glb["Time Trial"][2]+=1
        self.set_difficulty()
        self.board = Board(self.stage, self.stage, self.board.calculate_no_of_mines(self.stage, self.tt_difficulty))
        #print(f"Dimensions of board: {self.stage}x{self.stage}.\nStage: {self.stage - 5}.\nDifficulty: {self.tt_difficulty}")
        self.mines_left = self.board.calculate_no_of_mines(self.stage, self.tt_difficulty)
        self.board_done = False
        if self.tt_difficulty=="Hard" and not self.swapped_to_hard_tt:
            self.swapped_to_hard_tt = True
            return True

    def set_difficulty(self):
        #NOTE: the first stage is stage 6, as it is a 6x6 board
        #Testing new difficulties
        if self.stage < 10:
            self.tt_difficulty = "Easy"
        elif 10 <= self.stage <= 16:
            self.tt_difficulty = "Medium"
        elif 17 <= self.stage <= 23:
            self.tt_difficulty = "Hard"
        elif 24 <= self.stage <= 30:
            self.tt_difficulty = "Very Hard"

    def game_finished(self, final_score="", outcome="", mine_clicked=False):
        if self.database.user_signed_in:
            if self.game_mode=="Time Trial":
                self.database.add_tt_stage(self.stage - 5, mine_clicked, self.stopwatch)
                self.reset_top_10_info()
            elif self.game_mode=="Classic":
                if outcome=="WIN":
                    self.database.add_classic_time(final_score, self.difficulty)
                    self.reset_top_10_info()
                elif outcome=="LOSE":
                    self.database.add_classic_loss(final_score, self.difficulty)

    def reset_top_10_info(self):
        self.top_10_rank = self.database.top_10_rank
        self.no_1_status = self.database.no_1_status
        self.database.top_10_rank = 100
        self.database.no_1_status = ""

    def calculate_output_top_10_statement(self, current_communicator_text):
        if self.top_10_rank != 100:
            if not (self.game_mode == "Time Trial" and self.stage == 6):
                if self.no_1_status == "Reached":
                    top_10_statement = "NEW HIGHSCORE!"
                elif self.no_1_status == "Tied":
                    top_10_statement = "So close- you have tied with your best score"
                else:
                    suffixes = ["st", "nd", "rd"]
                    suffix = "th" if self.top_10_rank not in (1, 2, 3) else suffixes[self.top_10_rank - 1]
                    top_10_statement = f"Top 10 Score Achieved: {self.top_10_rank}{suffix}"
                return f"{current_communicator_text}\n{top_10_statement}"
        return current_communicator_text