from GameManager import GameManager
from tkinter import *

class GUI:
    def __init__(self):
        # creating main window
        self.Minesweeper = Tk()
        self.Minesweeper.title("Minesweeper")

        # creating frames
        self.main_menu = Frame(self.Minesweeper)
        self.game_frame = Frame(self.Minesweeper)

        # main menu widgets
        self.difficulty_button = Button()

        # game frame widgets
        self.communicator = Label()
        self.flags_left_counter = Label()
        self.cell_grid = Frame()

        # creating logic units
        self.game = GameManager()

    def create_main_menu(self):
        # main title
        Label(self.main_menu, text="MINESWEEPER", font=("Calibri Bold", 40), fg="black").grid(row=0, column=1)

        self.create_classic_button()

        # Player Level, Time Trial, Tutorial and Statistics buttons
        main_buttons = Frame(self.main_menu)
        main_buttons.grid(row= 2, column= 1)
        Button(main_buttons, text="Player Level", bg="yellow").grid(row=0, column=0, padx=5, pady=3)
        Button(main_buttons, text="Play - Time Trial", bg="#0181FF", command=lambda: self.start_game("Time Trial")).grid(row=0, column=1, padx=5, pady=3)
        Button(main_buttons, text="Tutorial", bg="purple").grid(row=1, column=0, padx=5, pady=3)
        Button(main_buttons, text="Statistics", bg="red").grid(row=1, column=1, padx=5, pady=3)
        for child in main_buttons.grid_slaves():
            child.config(font=("Calibri Bold", 24), width=20, height=2)

        # buttons in corners of main menu
        Button(self.main_menu, text="Settings", command= lambda: self.create_settings_window()).grid(row=0, column=0)
        Button(self.main_menu, text="Account", command= lambda: self.account_interaction()).grid(row=0, column=2)

        self.main_menu.pack()

    def create_classic_button(self):
        # creating frame that all classic button widgets go in
        classic_button_frame = Frame(self.main_menu, bg="green")
        classic_button_frame.grid(row=1, column=1, pady=7)

        # creating text saying 'Play - Classic'
        classic_label = Label(classic_button_frame, text="Play - Classic", font=("Calibri Bold", 30), bg="green", width=33, height=2)
        classic_label.grid(row=0, column=1, pady=5)
        
        # DIFFICULTY SWITCHER
        self.difficulty_switcher = Frame(classic_button_frame, bg = "#10401d")
        self.difficulty_switcher.grid(row=1, column=1)
        
        # difficulty button: need to access difficulty button later, so is stored as an attribute
        self.difficulty_button = Button(self.difficulty_switcher, text="Beginner", font=("Calibri Bold", 16), bg="#10401d", fg="white", width=12,
                                        command = lambda: self.change_difficulty())
        self.difficulty_button.grid(row=0, column=0)
        # rotate icon
        Button(self.difficulty_switcher, text="ROT", bg="#10401d", height=2, command=lambda: self.change_difficulty()).grid(row=0, column=1)

        # assigning start game command to entirety of classic button
        classic_button_frame.bind("<Button-1>", lambda event: self.start_game("Classic"))
        classic_label.bind("<Button-1>", lambda event: self.start_game("Classic"))

    def start_game(self, game_mode):
        # print(f"started {game_mode}")
        # swapping frames
        self.main_menu.forget()
        self.game_frame = Frame(self.Minesweeper)
        self.game_frame.pack()

        # creating the game frame widgets
        # title
        Label(self.game_frame, text="MINESWEEPER", font=("Calibri", 18)).grid(row=0, column=1)
        # textbox at bottom of screen
        self.communicator = Label(self.game_frame, text="Click a cell to start", font=("Calibri", 18), width=24, wraplength=300, height=2)
        self.communicator.grid(row=2, column=1, rowspan=4)
        
        self.flag_counter = Label(self.game_frame, text="", font=("Calibri", 20), width=2)
        self.flag_counter.grid(row=0, column=0)

        self.cell_grid = Frame(self.game_frame)
        self.cell_grid.grid(row=1, column=1)

        # starting the game
        if game_mode == "Classic":
            self.start_classic_mode(self.game.main_menu_difficulty)
        elif game_mode == "Time Trial":
            self.start_time_trial()

        # updating number of flags left after starting correct game mode
        self.flag_counter.config(text = str(self.game.board.flags_left))
    
    def change_difficulty(self):
        new_difficulty = self.game.difficulty_mapper[self.difficulty_button.cget("text")]
        self.difficulty_button.config(text = new_difficulty)
        self.game.main_menu_difficulty = new_difficulty

    def create_settings_window(self):
        pass

    def account_interaction(self):
        pass

    def start_classic_mode(self, difficulty):
        print(f"started classic mode at difficulty {difficulty}")
    
    def start_time_trial(self):
        print("started time trial")

gui = GUI()
gui.create_main_menu()
mainloop()

