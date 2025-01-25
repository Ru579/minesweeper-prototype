from Board import *

class GameManager:
    def __init__(self):
        self.game_started=False
        self.board = Board()
        #self.multi_revealed_occurred = False


    def start_classic_mode(self, difficulty):
        print("Start classic mode function called")
        self.game_started = True
        if difficulty == "Beginner":
            self.board = Board(8, 8, 2)
        elif difficulty == "Intermediate":
            self.board = Board(16, 16, 40)
        elif difficulty == "Expert":
            self.board = Board(16, 30, 99)


    def get_cell(self,x,y,info_needed):
        if info_needed=="value":
            return self.board.grid[x][y].value
        elif info_needed=="state":
            return self.board.grid[x][y].state


    def open_cell(self, x, y):
        print(f"Cell ({x},{y}) opened")
        self.board.open_cell(x,y,self.game_started)
        #self.multi_revealed_occurred = self.board.multi_reveal_occurred
        if not self.game_started:
            self.game_started = True
