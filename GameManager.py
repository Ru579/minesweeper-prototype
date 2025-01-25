from Board import *


class GameManager:
    def __init__(self):
        self.game_started = False
        self.board = Board()
        self.flag_difference = 0
        self.mines_left = 0
        self.difficulty = ""

    def start_classic_mode(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "Beginner":
            self.board = Board(8, 8, 10)
            self.mines_left=10
        elif difficulty == "Intermediate":
            self.board = Board(16, 16, 40)
            self.mines_left = 40
        elif difficulty == "Expert":
            self.board = Board(16, 30, 99)
            self.mines_left = 99

    def get_cell(self, x, y, info_needed):
        if info_needed == "value":
            return self.board.grid[x][y].value
        elif info_needed == "state":
            return self.board.grid[x][y].state

    def open_cell(self, x, y):
        print(f"Cell ({x},{y}) opened")
        self.board.open_cell(x, y, self.game_started)
        self.flag_difference = self.board.flag_difference
        self.board.flag_difference=0
        if not self.game_started:
            self.game_started = True


    def flag_cell(self, x, y):
        self.board.flag_cell(x,y)
        if self.board.grid[x][y].state=="Flagged":
            self.mines_left-=1
        elif self.board.grid[x][y].state!="Revealed":
            self.mines_left+=1

    def confuse_cell(self, x, y):
        cell_was_flagged = False
        if self.board.grid[x][y].state=="Flagged":
            cell_was_flagged = True
        self.board.confuse_cell(x,y)
        if cell_was_flagged:
            self.mines_left+=1



