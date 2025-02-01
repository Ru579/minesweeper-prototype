from Board import *
from DatabaseHandler import *


class GameManager:
    def __init__(self):
        self.game_started = False
        self.board = Board()
        self.flag_difference = 0
        self.mines_left = 0
        self.difficulty = ""
        self.game_has_been_won = False

    def start_classic_mode(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "Beginner":
            self.board = Board(8, 8, 10)
            self.mines_left = 10
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
        self.board.flag_difference = 0
        if not self.game_started:
            self.game_started = True
            self.game_has_been_won = False
        if self.board.revealed_cells == self.board.grid_width * self.board.grid_height - self.board.no_of_mines and not self.board.game_over:
            self.game_win()

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

    def game_win(self):
        self.game_has_been_won = True

    def user_information(self, username, time):  # where time is an array, 1st index is minutes, 2nd index is seconds
        add_user_info(username, time)
