from Board import Board
from time import sleep

class GameManager:
    def __init__(self):
        #initialising attributes
        self.board = Board(0,0,0)
        
        self.game_mode = ""
        self.game_started = False
        self.game_won = False

        self.user_can_interact = True

        # Time Trial attributes
        self.stage = 0 # stage corresponds to the length of one side of the square board
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

    def start_classic_mode(self, difficulty: str):
        self.difficulty = difficulty
        self.game_mode = "Classic"
        self.game_started = False
        self.game_won = False

        #creating board
        if difficulty == "Beginner":
            self.board = Board(5, 5, 3)
        elif difficulty == "Intermediate":
            self.board = Board(16,16, 40)
        elif difficulty == "Expert":
            self.board = Board(16, 30, 99)
    
    def start_time_trial(self):
        # initialising game state variables
        self.game_mode = "Time Trial"
        self.game_started = False
        self.game_won = False
        self.board_done = False
        self.swapped_to_hard_tt = False
        # the starting value of the timer
        self.minutes = 3
        self.seconds = 0

        self.stage = 6 # starting stage: first board has a length of 6
        self.tt_difficulty = "Easy"

        #creating the first board
        self.board = Board(self.stage, self.stage, self.calculate_mine_number())
    
    def calculate_mine_number(self):
        # returns the number of mines that should be on a square board of a specific length
        # floats determine mine concentration
        if self.tt_difficulty == "Easy":
            return round(0.13 * (self.stage ** 2))
        elif self.tt_difficulty == "Medium":
            return round(0.175 * (self.stage ** 2))
        elif self.tt_difficulty == "Hard":
            return round(0.206 * (self.stage ** 2))
        elif self.tt_difficulty == "Very Hard":
            return round(0.237 * (self.stage ** 2))
    
    def set_difficulty(self):
        # the first stage is stage 6, as stage = board length and the first board is a 6x6
        if self.stage < 10:
            self.tt_difficulty = "Easy"
        elif 10 <= self.stage <= 16:
            self.tt_difficulty = "Medium"
        elif 17 <= self.stage <= 23:
            self.tt_difficulty = "Hard"
        else:
            self.tt_difficulty = "Very Hard"
    
    def next_tt_stage(self):
        self.timer_on = False # stopping timer from running until the user first clicks on a cell on the new board
        self.time_to_be_added = True
        self.stage += 1
        
        # creating the next board after setting the difficulty (difficulty depends on stage reached)
        self.previous_tt_difficulty = self.tt_difficulty
        self.set_difficulty()
        self.board = Board(self.stage, self.stage, self.calculate_mine_number())

        # resetting whether the board has been completed since a new board has been created
        self.board_done = False

        if not self.swapped_to_hard_tt and self.stage == "Hard":
            self.swapped_to_hard_tt = True
    
    def open_cell(self, x: int, y: int):
        self.board.open_cell(x, y, self.game_started)
        
        #starting the timer after the first click on the board
        if not self.game_started:
            self.game_started = True
            self.timer_on = True
        
        self.board_done_check()
    
    
    def board_done_check(self):
        # if user has revealed all non-mine cells
        if self.board.revealed_cells == self.board.grid_height * self.board.grid_width - self.board.no_of_mines and not self.board.game_over:
            if self.game_mode == "Classic":
                self.game_won = True
            elif self.game_mode == "Time Trial":
                self.board_done = True
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
            
    def run_game(self):
        if self.game_mode == "Classic":
            self.show_grid()
            self.user_interation()
        elif self.game_mode == "Time Trial":
            while not self.board.game_over:
                self.show_grid()
                self.user_interation()
                self.next_tt_stage()
                self.user_can_interact = True

    def show_grid(self):
        print(f"Flags left: {self.board.flags_left}")
        for row in range(self.board.grid_height):
            current_row = ""
            for column in range(self.board.grid_width):
                state = self.board.grid[row][column].state
                #representing hidden cells with black 'X's
                if state == "Hidden":
                    current_row += f"\033[30m X \033[0m"
                #representing revealed cells with their value in blue
                elif state == "Revealed":
                    current_row += f"\033[94m {self.board.grid[row][column].value} \033[0m"
                # representing flagged cells with their value in dark red
                elif state == "Flagged":
                    current_row += f"\033[31m F \033[0m"
                #representing confused cells with their value in dark green
                elif state == "Confused":
                    current_row += f"\033[32m C \033[0m"
            print(current_row)

    def user_interation(self):
        player_active = True
        while player_active and self.user_can_interact and not self.board.game_over:
            game_action = int(input("(1): Open Cell\n(2): Flag Cell\n(3): Confuse Cell\n(4): End Interaction\n"))
            if game_action != 4:
                x_coordinate = int(input("Enter x coordinate:"))
                y_coordinate = int(input("Enter y coordinate:"))
            if game_action == 1:
                self.open_cell(x_coordinate, y_coordinate)
            elif game_action == 2:
                self.board.flag_cell(x_coordinate, y_coordinate)
            elif game_action == 3:
                self.board.confuse_cell(x_coordinate, y_coordinate)
            elif game_action == 4:
                player_active = False
            self.show_grid()
        if self.game_won:
            print("GAME HAS BEEN WON!")
        elif self.game_mode == "Time Trial" and self.board_done:
            print("NEXT STAGE!")
        elif self.board.game_over:
            print("GAME OVER!")
            
#main code
game = GameManager()
game_mode_selection = input("Select Classic (C) or Time Trial (T):\n").upper()
if game_mode_selection == "C":
    game.start_classic_mode("Beginner")
elif game_mode_selection == "T":
    game.start_time_trial()
game.run_game()

#game.stage = 16
#game.tt_difficulty = "Medium"
#print(f"Time- {game.minutes:02}:{game.seconds:02}")
#game.next_tt_stage()
#game.update_countdown_timer()
#print(f"Time- {game.minutes:02}:{game.seconds:02}")

#game.timer_on = False
#game.time_to_be_added = True
#game.minutes = 2
#game.seconds = 35
#game.tt_difficulty = "Medium"
#print(f"Time- {game.minutes:02}:{game.seconds:02}")
#game.update_countdown_timer()
#print(f"Time- {game.minutes:02}:{game.seconds:02}")

#for _ in range(100):
#    print(f"Time- {game.minutes:02}:{game.seconds:02}")
#    sleep(1)
#    game.update_countdown_timer()




