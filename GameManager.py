from Board import Board

class GameManager:
    def __init__(self):
        #initialising attributes
        self.board = Board(0,0,0)
        
        self.game_mode = ""
        self.game_started = False
        self.game_won = False
    
    def start_classic_mode(self, difficulty: str):
        self.difficulty = difficulty
        self.game_mode = "Classic"

        #creating board
        if difficulty == "Beginner":
            self.board = Board(8, 8, 10)
        elif difficulty == "Intermediate":
            self.board = Board(16,16, 40)
        elif difficulty == "Expert":
            self.board = Board(16, 30, 99)
    
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
            self.user_can_interact = False
            
    def run_game(self):
        self.show_grid()
        self.user_interation()
    
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
        while player_active:
            game_action = int(input("(1): Open Cell\n(2): Flag Cell\n(3): Confuse Cell\n(4): End Interaction\n"))
            if game_action != 4:
                x_coordinate = int(input("Enter x coordinate:"))
                y_coordinate = int(input("Enter y coordinate:"))
            if game_action == 1:
                self.open_cell(x_coordinate, y_coordinate)
                if self.board.game_over:
                    print("GAME OVER")
            elif game_action == 2:
                self.board.flag_cell(x_coordinate, y_coordinate)
            elif game_action == 3:
                self.board.confuse_cell(x_coordinate, y_coordinate)
            elif game_action == 4:
                player_active = False
            self.show_grid()
            
#main code
game = GameManager()
game.start_classic_mode("Beginner")
game.run_game()


