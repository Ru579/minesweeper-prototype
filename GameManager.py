from Board import Board

class GameManager:
    def __init__(self):
        #initialising attributes
        self.board = Board()
        
        self.game_started = False
        self.game_mode = ""
    
    def start_classic_mode(self, difficulty):
        self.difficulty = difficulty
        self.game_mode = "Classic"

        #creating board
        if difficulty == "Beginner":
            self.board = Board(8, 8, 10)
        elif difficulty == "Intermediate":
            self.board = Board(16,16, 40)
        elif difficulty == "Expert":
            self.board = Board(16, 30, 99)
    
    def open_cell(self, x, y):
        self.board.open_cell(x, y, self.game_started)
        
        #starting the timer after the first click on the board
        if not self.game_started:
            self.timer_on = True
        
        self.board_done_check()
    
    
    def board_done_check(self):
        pass
        