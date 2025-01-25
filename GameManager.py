#Needs to have the attribute game_started, which it passes into board during the open_cell function
#It then, after calling the board.open_cell() function, needs to set its game_started attribute to True


from Board import *

class GameManager:
    def __init__(self):
        self.game_started=False
        self.board = Board()
        self.multi_revealed_occurred = False


    def start_classic_mode(self, difficulty):
        self.game_started = True
        if difficulty == "Beginner":
            self.board = Board(8, 8, 10)
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
        self.board.open_cell(x,y,self.game_started)
        self.multi_revealed_occurred = self.board.multi_reveal_occurred
        self.game_started = True




my_game = GameManager()
my_game.start_classic_mode("Beginner")