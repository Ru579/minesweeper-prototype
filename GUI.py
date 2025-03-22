from GameManager import *
from Settings import *
from LoginGUI import *


class GUI:
    def __init__(self):
        # creating main window
        self.Minesweeper = Tk()
        self.Minesweeper.title("Minesweeper")

        # creating logic units
        self.game = GameManager()
        self.settings = Settings(self.Minesweeper)
        self.loginGUI = LoginGUI(self.Minesweeper, self.game.database)

        # creating frames
        self.main_menu = Frame(self.Minesweeper)
        self.game_frame = Frame(self.Minesweeper)
        self.game_finished_window = Frame(self.Minesweeper)

        # creating main_menu widgets
        self.difficulty_button = Button()

        # creating game_frame widgets
        self.cell_grid = Frame(self.game_frame)
        self.mines_left_counter = Label(self.game_frame)
        self.countup_timer = Label(self.game_frame, text="")
        self.countdown_timer = Label(self.game_frame)
        self.communicator = Label(self.game_frame)
        self.retry_button = Button(self.game_frame)

        # creating array of buttons
        self.tiles = []

        # getting images
        self.cell_images = {
            "hidden_cell_image": Image.open("hidden_cell_darker.png"),
            "mine_image": Image.open("mine_cell_red.png"),
            "flagged_cell_image": Image.open("minesweeper_flag.png"),
            "incorrect_flagged_image": Image.open("incorrect_flag_new.png"),
            "confused_cell_image": Image.open("confuse_cell_v3_green.png"),
            "highlighted_hidden_cell_image": Image.open("highlighted_hidden_cell.png"),
            "highlighted_flagged_cell_image": Image.open("highlighted_minesweeper_flag.png"),
            "highlighted_confused_cell_image": Image.open("highlighted_confuse_cell_v3_green.png")
        }
        self.formatted_cell_images = {}
        # cell_images are the opened images, not resized or formatted

        self.cell_number_images = []
        for i in range(9):
            current_image = Image.open(f"{i}_cell_new.png")
            self.cell_number_images.append(current_image)
        self.formatted_number_images = []
        # cell_number_images are the images of the numbers to go on buttons. not resized or formatted

        # begins program by creating the main_menu
        self.create_main_menu()

    def create_main_menu(self):
        # configuring the geometry and rows of the main menu
        # self.main_menu.geometry("1000x1000")
        weights = [2, 3, 2, 2, 1, 2, 1]
        for i in range(4):
            if i != 3:
                self.main_menu.columnconfigure(i, weight=weights[i])
            self.main_menu.rowconfigure(i, weight=weights[i + 3])

        Label(self.main_menu, text="MINESWEEPER", font=("Calibri", 40), bg="white", fg="black").grid(row=0, column=1, pady=7)

        # creating classic button
        classic_button = Frame(self.main_menu, bg="green")
        for i in range(3):
            classic_button.columnconfigure(i, weight=1)
        classic_button.rowconfigure(0, weight=2)
        classic_button.rowconfigure(1, weight=1)
        classic_label = Label(classic_button, text="Classic", font=("Calibri", 30), bg="green", width=33, height=2)
        classic_label.grid(row=0, column=1)
        # need to access difficulty button later, so it is stored as an attribute
        self.difficulty_button = Button(classic_button, text="Beginner", font=("Calibri", 16), bg="#10401d", fg="white", width=12,
                                        command=lambda: self.change_difficulty(self.difficulty_button.cget("text")))
        self.difficulty_button.grid(row=1, column=1)
        classic_button.bind("<Button-1>", lambda event: self.start_game("Classic"))
        classic_label.bind("<Button-1>", lambda event: self.start_game("Classic"))
        classic_button.grid(row=1, column=1, pady=7)

        # other main_menu widgets
        game_modes = Frame(self.main_menu)
        game_modes.grid(row=2, column=1)
        Button(self.main_menu, text="Tutorial", font=("Calibri", 16), bg="green", width=11).grid(row=3, column=0)
        Label(self.main_menu, text="PROTO", font=("Calibri", 16), bg="grey", width=10).grid(row=3, column=2)
        Button(self.main_menu, text="Settings:gear_icon", font=("Calibri", 12), bg="grey", fg="blue", height=2, width=20,
               command=lambda: self.settings.create_settings_window(self.main_menu, self.Minesweeper)).grid(
            row=0, column=0)
        # MAY NEED TO BE CHANGED- currently, instantiation of loginGUI is what creates the login button
        #self.game.loginGUI = LoginGUI(self.main_menu, self.Minesweeper)
        self.loginGUI.create_profile(self.main_menu)


        # central buttons (below classic button)
        Button(game_modes, text="Leaderboard", font=("Calibri", 24), bg="yellow", width=20, height=2, pady=8).grid(row=0, column=0, padx=5, pady=3)
        Button(game_modes, text="Time Trial", font=("Calibri", 24), bg="blue", width=20, height=2, pady=8, command=lambda: self.start_game("Time Trial")).grid(row=0, column=1, padx=5, pady=3)
        Button(game_modes, text="Tips", font=("Calibri", 24), bg="purple", width=20, height=2, pady=8).grid(row=1, column=0, padx=5, pady=3)
        Button(game_modes, text="Statistics", font=("Calibri", 24), bg="red", width=20, height=2, pady=8).grid(row=1, column=1, padx=5, pady=3)

        #TEMPORARY
        Button(self.main_menu, text="Delete current account?", bg="red", command=lambda: self.loginGUI.delete_user()).grid(row=4,column=2)

        self.main_menu.pack()

    def change_difficulty(self, difficulty):
        if difficulty == "Beginner":
            self.difficulty_button.config(text="Intermediate")
        elif difficulty == "Intermediate":
            self.difficulty_button.config(text="Expert")
        elif difficulty == "Expert":
            self.difficulty_button.config(text="Beginner")

    def start_game(self, game_mode, difficulty=""):
        self.main_menu.forget()
        self.game_frame = Frame(self.Minesweeper)
        self.game_frame.pack()

        title = Label(self.game_frame, text="MINESWEEPER.PROTO", font=("Calibri", 20))
        title.grid(row=0, column=1)

        self.communicator = Label(self.game_frame, text="Click a cell to start", font=("Calibri", 18), width=24, wraplength=300, height=2)
        self.communicator.grid(row=2, column=1, rowspan=4) #rowspan = 3

        self.mines_left_counter = Label(self.game_frame, text="", font=("Calibri", 20), width=2)
        self.mines_left_counter.grid(row=0, column=0)

        self.cell_grid = Frame(self.game_frame)
        self.cell_grid.grid(row=1, column=1)

        if game_mode == "Classic":
            if not difficulty:  # if we are starting a classic game from the main menu
                self.start_classic_mode(self.difficulty_button.cget("text"))
            else:  # we have used the retry function, and are passing in a difficulty
                self.start_classic_mode(difficulty)
        if game_mode == "Time Trial":
            self.start_time_trial()

        self.mines_left_counter.config(text=str(self.game.mines_left))

    def start_classic_mode(self, difficulty):
        self.game.start_classic_mode(difficulty)

        self.countup_timer = Label(self.game_frame, text="00:00", font=("Calibri", 20), width=5)
        self.countup_timer.grid(row=0, column=2)

        # self.mines_left_counter = Label(self.game_frame, text=str(self.game.mines_left), font=("Calibri", 20), width=2)
        # self.mines_left_counter.grid(row=0, column=0)

        if self.formatted_number_images:
            self.formatted_number_images = []

        # setting cell image dimensions
        if self.game.difficulty == "Beginner":
            cell_length = 62  # could change to 65
        else:
            cell_length = 42  # could change to 45

        # formatting and resizing images
        for image in self.cell_images:
            self.formatted_cell_images[image] = self.cell_images[image].resize((cell_length, cell_length))
            self.formatted_cell_images[image] = ImageTk.PhotoImage(self.formatted_cell_images[image])
        for number in range(9):
            temp_number_image = self.cell_number_images[number].resize((cell_length, cell_length))
            temp_number_image = ImageTk.PhotoImage(temp_number_image)
            self.formatted_number_images.append(temp_number_image)

        # making all GUI tile buttons
        self.tiles = [[Button(self.cell_grid) for _ in range(0, self.game.board.grid_width)] for _ in range(0, self.game.board.grid_height)]

        for i in range(0, self.game.board.grid_height):
            for j in range(0, self.game.board.grid_width):
                tile = Button(self.cell_grid)
                tile.config(command=lambda row=i, column=j: self.ui_open_cell(row, column))
                tile.bind("<Button-2>", lambda event, row=i, column=j: self.ui_confuse_cell(row, column))
                tile.bind("<Button-3>", lambda event, row=i, column=j: self.ui_flag_cell(row, column))

                if self.game.difficulty == "Beginner":
                    tile.config(image=self.formatted_cell_images["hidden_cell_image"], width=60, height=60)
                elif self.game.difficulty == "Intermediate" or self.game.difficulty == "Expert":
                    tile.config(image=self.formatted_cell_images["hidden_cell_image"], width=40, height=40)

                tile.grid(row=i + 1, column=j + 1)
                self.tiles[i][j] = tile
        self.game.user_can_interact = True

    def start_time_trial(self):
        self.game.start_time_trial()

        self.countdown_timer = Label(self.game_frame, text="03:00", font=("Calibri", 20), width=5)
        self.countdown_timer.grid(row=0, column=2)

        # self.mines_left_counter = Label(self.game_frame, text=str(self.game.mines_left), font=("Calibri", 20), width=2)
        # self.mines_left_counter.grid(row=0, column=0)

        if self.formatted_number_images:
            self.formatted_number_images = []

        # resizing and formatting images
        for image in self.cell_images:
            self.formatted_cell_images[image] = self.cell_images[image].resize((62, 62))
            self.formatted_cell_images[image] = ImageTk.PhotoImage(self.formatted_cell_images[image])
        for number in range(9):
            temp_number_image = self.cell_number_images[number].resize((62, 62))
            temp_number_image = ImageTk.PhotoImage(temp_number_image)
            self.formatted_number_images.append(temp_number_image)

        self.make_tt_board()

    def make_tt_board(self, swapped_to_hard=False):
        self.game.game_started = False
        for widget in self.cell_grid.winfo_children():
            widget.destroy()
        self.cell_grid.destroy()
        self.cell_grid = Frame(self.game_frame)
        self.cell_grid.grid(row=1, column=1)
        self.tiles = [[Button(self.cell_grid) for _ in range(0, self.game.board.grid_width)] for _ in range(0, self.game.board.grid_height)]

        # reformatting and resiizng images if now in hard mode
        if swapped_to_hard:
            if self.formatted_number_images:
                self.formatted_number_images = []
            for image in self.cell_images:
                self.formatted_cell_images[image] = self.cell_images[image].resize((42, 42))
                self.formatted_cell_images[image] = ImageTk.PhotoImage(self.formatted_cell_images[image])
            for number in range(9):
                temp_number_image = self.cell_number_images[number].resize((42, 42))
                temp_number_image = ImageTk.PhotoImage(temp_number_image)
                self.formatted_number_images.append(temp_number_image)

        # creates all buttons of the board
        for i in range(0, self.game.board.grid_height):
            for j in range(0, self.game.board.grid_width):
                tile = Button(self.cell_grid)
                tile.config(command=lambda row=i, column=j: self.ui_open_cell(row, column))
                tile.bind("<Button-2>", lambda event, row=i, column=j: self.ui_confuse_cell(row, column))
                tile.bind("<Button-3>", lambda event, row=i, column=j: self.ui_flag_cell(row, column))
                if self.game.tt_difficulty == "Easy" or self.game.tt_difficulty == "Medium":
                    tile.config(image=self.formatted_cell_images["hidden_cell_image"], width=60, height=60)
                else:
                    tile.config(image=self.formatted_cell_images["hidden_cell_image"], width=40, height=40)
                tile.grid(row=i + 1, column=j + 1)
                self.tiles[i][j] = tile
        self.game.user_can_interact = True

    def next_tt_stage(self):
        self.communicator.config(text="Next Stage")
        self.game.time_to_be_added = True
        swapped_to_hard = self.game.next_tt_stage()
        self.game.timer_on = False
        self.mines_left_counter.config(text=self.game.mines_left)
        self.game_frame.after(500, lambda: self.make_tt_board(swapped_to_hard))

    def update_countup_timer(self, minutes, seconds):
        if self.game.timer_on:
            seconds += 1
            if seconds == 60:
                seconds = 0
                minutes += 1
            self.countup_timer.config(text=f"{minutes:02}:{seconds:02}")
            self.countup_timer.after(1000, lambda: self.update_countup_timer(minutes, seconds))

    def update_countdown_timer(self, minutes, seconds):
        self.game.time_change_type = ""
        minutes, seconds = self.game.update_countdown_timer(minutes, seconds)
        if self.game.time_change_type == "Time Added" or self.game.time_change_type == "Time Normal":
            self.countdown_timer.config(text=f"{minutes:02}:{seconds:02}")
            self.countdown_timer.after(1000, lambda: self.update_countdown_timer(minutes, seconds))
        elif self.game.time_change_type == "Time Game Over":
            self.countdown_timer.config(text="00:00")
            self.do_game_over(1800)
        elif self.game.tt_running:
            self.countdown_timer.after(200, lambda: self.update_countdown_timer(minutes, seconds))

    def ui_open_cell(self, x, y):
        if self.game.user_can_interact:
            self.game.open_cell(x, y)
            self.update_ui()
            self.communicator.config(text="")

            # if game hasn't started yet, starts the respective timers
            if not self.game.game_started:
                self.game.game_started = True
                if self.game.game_mode == "Classic":
                    self.countup_timer.after(1000, lambda: self.update_countup_timer(0, 0))
                if self.game.game_mode == "Time Trial" and not self.game.tt_running:
                    self.game.tt_running = True
                    self.countdown_timer.after(1000, lambda: self.update_countdown_timer(3, 0))

            # if player hasn't placed enough flags
            if self.game.flag_difference < 0:
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if self.game.board.in_bounds(i, j):
                            state = self.game.get_cell(i, j, "state")
                            if state == "Hidden" or state == "Confused":
                                self.tiles[i][j].config(image=self.formatted_cell_images[f"highlighted_{state.lower()}_cell_image"])
                                self.return_cell_to_normal(i, j, normal_state=state)
                self.communicator.config(text=f"Cell has {-1 * self.game.flag_difference} too few flags.")

            # if player has placed too many flags
            if self.game.flag_difference > 0:
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if self.game.board.in_bounds(i, j) and self.game.get_cell(i, j, "state") == "Flagged":
                            self.tiles[i][j].config(image=self.formatted_cell_images["highlighted_flagged_cell_image"])
                            self.return_cell_to_normal(i, j, normal_state="Flagged")
                self.communicator.config(text=f"Cell has {self.game.flag_difference} too many flags.")

            self.game_state_check()

    def return_cell_to_normal(self, row, column, normal_state):
        self.tiles[row][column].after(500, lambda x=row, y=column: self.fix_cell_colour(x, y, normal_state))

    def fix_cell_colour(self, row, column, normal_state):
        state = self.game.get_cell(row, column, "state")
        # states = ["Hidden", "Flagged", "Confused"]
        for cell_state in "Hidden", "Flagged", "Confused":
            if normal_state == cell_state and state == cell_state:
                self.tiles[row][column].config(image=self.formatted_cell_images[f"{cell_state.lower()}_cell_image"])

    def ui_flag_cell(self, x, y):
        if self.game.user_can_interact:
            self.game.flag_cell(x, y)

            # if a cell has been flagged
            if self.game.get_cell(x, y, "state") == "Flagged":
                self.tiles[x][y].config(image=self.formatted_cell_images["flagged_cell_image"])

            # if a cell has been unflagged
            elif self.game.get_cell(x, y, "state") == "Hidden":
                self.tiles[x][y].config(image=self.formatted_cell_images["hidden_cell_image"])
                # if a cell has remained hidden because the board class has determined that the player has ran out of flags
                if self.game.board.not_enough_flags:
                    self.communicator.config(text="Not enough flags")
                    self.communicator.after(500, lambda: self.communicator.config(text=""))
                    self.game.board.not_enough_flags = False

            # updates mines_left_counter accordingly
            self.mines_left_counter.config(text=str(self.game.mines_left))

    def ui_confuse_cell(self, x, y):
        if self.game.user_can_interact:
            self.game.confuse_cell(x, y)

            if self.game.get_cell(x, y, "state") == "Confused":
                self.tiles[x][y].config(image=self.formatted_cell_images["confused_cell_image"])
            if self.game.get_cell(x, y, "state") == "Hidden":
                self.tiles[x][y].config(image=self.formatted_cell_images["hidden_cell_image"])

            # updates mines_left_counter accordingly
            self.mines_left_counter.config(text=str(self.game.mines_left))

    def update_ui(self):
        for i in range(0, self.game.board.grid_height):
            for j in range(0, self.game.board.grid_width):
                if self.game.get_cell(i, j, "state") == "Revealed":
                    if self.game.get_cell(i, j, "value") == "*":
                        self.tiles[i][j].config(image=self.formatted_cell_images["mine_image"])
                    elif self.game.get_cell(i, j, "value") == "0":
                        self.tiles[i][j].config(image=self.formatted_number_images[0])
                    else:  # check why a value of 0 can't be included in the following line
                        self.tiles[i][j].config(image=self.formatted_number_images[int(self.game.get_cell(i, j, "value"))])

    def game_state_check(self):
        if self.game.board.game_over:
            self.game.user_can_interact = False
            self.game.tt_running = False
            self.do_game_over()
            self.game.game_started = False
        elif self.game.game_mode == "Classic":
            if self.game.game_has_been_won:
                self.game.game_finished(self.countup_timer.cget("text"), "WIN")

                # not 100% sure about the following line
                self.game.timer_on = False

                self.communicator.config(text="Congratulations!")
                self.game.game_started = False
                if self.settings.user_settings["create_game_finished_window"]:
                    self.game_frame.after(500, lambda: self.create_game_finished_window("WIN"))
                else:
                    self.show_top_10_rank()
                    self.make_quick_replay_buttons()
                    #self.show_top_10_rank()

        elif self.game.game_mode == "Time Trial":
            if self.game.board_done:
                self.game.timer_on = False  # stops timer from ticking down when swapping stages (I think)
                self.communicator.config(text="Next Stage")
                self.next_tt_stage()

    def do_game_over(self, delay=1250):
        self.game.timer_on = False

        # if player ran out of time
        if self.game.game_mode == "Time Trial" and self.countdown_timer.cget("text") == "00:00":
            self.game.user_can_interact = False
            self.game.game_finished()
            self.communicator.config(text="GAME OVER: Time Ran Out!")
            if not self.settings.user_settings["create_game_finished_window"]:
                # create a button to view mines
                view_mines_button = Button(self.game_frame, bg="yellow", text="View Mines", font=("Calibri", 15), width=10, command=lambda: self.toggle_all_mine_reveal(view_mines_button))
                view_mines_button.grid(row=3, column=2)
        #if player clicked a mine in either time trial or classic
        else:
            self.game.game_finished(self.countup_timer.cget("text"), "LOSE", True)

            self.communicator.config(text="GAME OVER!")
            self.toggle_all_mine_reveal()

        if self.settings.user_settings["create_game_finished_window"]:
            self.game_frame.after(delay, lambda: self.create_game_finished_window("LOSE"))
        else:
            if self.game.game_mode=="Time Trial":
                self.show_top_10_rank()
            self.make_quick_replay_buttons()

    def show_top_10_rank(self):
        #if self.game.top_10_rank != 100:
        #    #removes rowspan from communicator so that it doesn't merge with the label showing what stage was reached and the time taken
        #    if self.game.game_mode=="Time Trial":
        #        current_text = self.communicator.cget("text")
        #        self.communicator.destroy()
        #        self.communicator = Label(self.game_frame, font=("Calibri", 18), text=current_text, width=24, wraplength=300, height=3)  # height = 2
        #        self.communicator.grid(row=2, column=1)

        #    if not (self.game.game_mode == "Time Trial" and self.game.stage == 6):
        #        if self.game.no_1_status == "Reached":
        #            top_10_statement = "NEW HIGHSCORE!"
        #        elif self.game.no_1_status == "Tied":
        #            top_10_statement = "So close- you have tied with your best score"
        #        else:
        #            suffixes = ["st", "nd", "rd"]
        #            suffix = "th" if self.game.top_10_rank not in (1, 2, 3) else suffixes[self.game.top_10_rank - 1]
        #            top_10_statement = f"Top 10 Score Achieved: {self.game.top_10_rank}{suffix}"
        #        self.communicator.config(text=self.communicator.cget("text")+f"\n{top_10_statement}")

        top_10_statement = self.game.calculate_output_top_10_statement(self.communicator.cget("text"))

        # removes rowspan from communicator so that it doesn't merge with the label showing what stage was reached and the time taken
        if self.game.game_mode == "Time Trial":
            current_text = self.communicator.cget("text")
            self.communicator.destroy()
            self.communicator = Label(self.game_frame, font=("Calibri", 18), text=current_text, width=24, wraplength=300, height=3)  # height = 2
            self.communicator.grid(row=2, column=1)
        self.communicator.config(text=top_10_statement)



    def toggle_all_mine_reveal(self, button=None):
        # reveal all cells that are mines
        if not self.game.mines_revealed:
            for i in range(self.game.board.grid_height):
                for j in range(self.game.board.grid_width):
                    if self.game.get_cell(i, j, "value") == "*" and self.game.get_cell(i, j, "state") != "Flagged":  # is a mine that was not flagged
                        self.tiles[i][j].config(image=self.formatted_cell_images["mine_image"])
                    elif self.game.get_cell(i, j, "value") != "*" and self.game.get_cell(i, j, "state") == "Flagged":  # is a flagged cell and was not a mine
                        self.tiles[i][j].config(image=self.formatted_cell_images["incorrect_flagged_image"])
            # if self.game.game_mode == "Time Trial" and widgets.countdown_timer.cget("text") == "00:00":
            if button is not None:
                button.config(text="Hide Mines")
            self.game.mines_revealed = True

        # hide all mines
        else:
            for i in range(self.game.board.grid_height):
                for j in range(self.game.board.grid_width):
                    if self.game.get_cell(i, j, "state") == "Confused":  # if a cell is confused, show it to be so (if changed by mines being revealed)
                        self.tiles[i][j].config(image=self.formatted_cell_images["confused_cell_image"])
                    elif self.game.get_cell(i, j, "value") != "*" and self.game.get_cell(i, j, "state") == "Flagged":  # a cell has been shown to have been incorrectly flagged
                        self.tiles[i][j].config(image=self.formatted_cell_images["flagged_cell_image"])
                    elif self.game.get_cell(i, j, "value") == "*" and self.game.get_cell(i, j, "state") != "Flagged":  # a cell was a mine but was not flagged
                        self.tiles[i][j].config(image=self.formatted_cell_images["hidden_cell_image"])
                    # elif self.game.get_cell(i,j,"state")=="Confused":
                    #    tiles[i][j].config(image=current_cell_images["confused_cell_image"])
            button.config(text="View Mines")
            self.game.mines_revealed = False

    def make_quick_replay_buttons(self):
        # creating retry button, without its command assigned
        self.retry_button = Button(self.game_frame, text="Retry?", bg="blue", fg="white", font=15, width=10)  # command=lambda: retry(game.game_mode))
        self.retry_button.grid(row=2, column=0)

        # creaing a return to menu button
        Button(self.game_frame, text="Menu", bg="blue", fg="white", font=15, width=10, command=lambda: self.return_to_menu(self.game_frame)).grid(row=2, column=2)
        if self.game.game_mode == "Classic":
            difficulty_changer = Label(self.game_frame, text="Change Difficulty?", bg="green", fg="white", font=15, width=15)
            difficulty_changer.bind("<Button-1>", lambda event: self.change_retry_difficulty(difficulty_changer))
            difficulty_changer.grid(row=3, column=0)
            self.retry_button.bind("<Button-1>", lambda event: self.retry(difficulty_changer))
        else:
            self.retry_button.bind("<Button-1>", lambda event: self.retry())
            Label(self.game_frame, text=f"Stage: {self.game.stage - 5}\nYou lasted for- {self.game.stopwatch // 60:02}:{self.game.stopwatch % 60:02}",
                  font=("Calibri Bold", 15), bg="dark grey", fg="green").grid(row=3, column=1)

    def retry(self, label=None, destroy_window=False):
        if self.game.game_mode == "Classic":
            # text = label.cget("text")
            # retries at the current difficulty, unless the player has changed what difficulty they wish to play
            if label.cget("text") == "Change Difficulty?":
                difficulty = self.game.difficulty
            else:
                difficulty = label.cget("text")

            self.game_frame.destroy()
            self.start_game(self.game.game_mode, difficulty)

        # if in time trial, just retry immediately
        else:
            self.game_frame.destroy()
            self.start_game(self.game.game_mode)

        # if retrying from game_finished_window, that window will then be destroyed
        if destroy_window:
            self.game_finished_window.destroy()

    def change_retry_difficulty(self, button):
        difficulties = Menu(self.game_frame, tearoff=False)
        for difficulty in "Beginner", "Intermediate", "Expert":
            difficulties.add_command(label=difficulty, command=lambda current_difficulty = difficulty: button.config(text=current_difficulty))
        try:
            x = button.winfo_rootx()
            y = button.winfo_rooty()
            difficulties.tk_popup(x, y)
        finally:
            difficulties.grab_release()

    def create_game_finished_window(self, outcome):
        # calculating final time- how long the player took
        final_time = []
        if self.game.game_mode == "Classic":
            final_time = [self.countup_timer.cget("text")[0:2], self.countup_timer.cget("text")[3:5]]
        elif self.game.game_mode == "Time Trial":
            final_time = [f"{self.game.stopwatch // 60:02}", f"{self.game.stopwatch % 60:02}"]

        self.game.timer_on = False

        # Swaps frames to game_finished window
        self.game_frame.forget()
        self.game_finished_window = Frame(self.Minesweeper)
        self.game_finished_window.pack()

        # configures rows and columns
        for i in range(4):
            self.game_finished_window.columnconfigure(i, weight=1)
            current_weight = 3 if (i == 0 or i == 3) else 2
            self.game_finished_window.rowconfigure(i, weight=current_weight)

        if self.game.game_mode == "Classic":
            self.classic_game_over_window(outcome, final_time)
        elif self.game.game_mode == "Time Trial":
            self.tt_game_over_window(final_time)

    def classic_game_over_window(self, outcome, final_time):
        # creates text confirming outcome and final time
        if outcome == "WIN":
            Label(self.game_finished_window, text=f"Your time was:\n {final_time[0]}:{final_time[1]}", font=("Calibri", 16)).grid(row=0, column=1)
        elif outcome == "LOSE":
            Label(self.game_finished_window, text=f"GAME OVER!\nYour time was {final_time[0]}:{final_time[1]}", font=("Calibri", 16)).grid(row=0, column=1)

        game_finished_options = Frame(self.game_finished_window)
        game_finished_options.grid(row=1, column=1)

        # make retry button
        retry_button = Button(game_finished_options, text="Retry?", bg="blue", fg="white", font=("Calibri", 16), width=15, command=lambda: self.retry(difficulty_changer, destroy_window=True))
        retry_button.grid(row=0, column=0)

        # make button that changes difficulty
        difficulty_changer = Button(game_finished_options, text="Change Difficulty?", bg="green", fg="white", font=("Calibri", 16), width=15,
                                    command=lambda: self.change_retry_difficulty(difficulty_changer))
        # difficulty_changer.bind("<Button-1>", lambda event: self.change_retry_difficulty(difficulty_changer))
        difficulty_changer.grid(row=0, column=1)

        Button(game_finished_options, text="View Board?", font=("Calibri", 16), width=15, command=lambda: self.view_board()).grid(row=1, column=0)
        Button(game_finished_options, text="Close", font=("Calibri", 16), width=15, command=lambda: self.return_to_menu(self.game_finished_window)).grid(row=1, column=1)

        # game_finished_options.grid(row=1, column=1)

    def tt_game_over_window(self, final_time):
        # Label(self.game_finished_window, text=f"You got to stage {self.game.stage - 5}\nYou lasted for:\n {self.game.stopwatch // 60:02}:{self.game.stopwatch % 60:02}", font=("Calibri", 16)).grid(row=0, column=1)
        Label(self.game_finished_window, text=f"You got to stage {self.game.stage - 5}\nYou lasted for:\n {final_time[0]}:{final_time[1]}", font=("Calibri", 16)).grid(row=0, column=1)

        retry_button = Button(self.game_finished_window, text="Retry?", bg="blue", fg="white", font=15, width=6, command=lambda: self.retry(destroy_window=True))
        retry_button.grid(row=1, column=1)

        Button(self.game_finished_window, text="View Board?", font=("Calibri", 16), command=lambda: self.view_board()).grid(row=2, column=1)
        Button(self.game_finished_window, text="Close", font=("Calibri", 16), command=lambda: self.return_to_menu(self.game_finished_window)).grid(row=3, column=1)

    def view_board(self):
        self.game_finished_window.destroy()
        self.game_frame.pack()
        if self.game.game_mode == "Time Trial" and self.countdown_timer.cget("text") == "00:00":
            self.toggle_all_mine_reveal()
        Button(self.game_frame, text="Menu", bg="blue", fg="white", font=15, width=10, command=lambda: self.return_to_menu(self.game_frame)).grid(row=2, column=2)
        view_mines_button = Button(self.game_frame, text="Hide Mines", bg="yellow", font=("Calibri", 15), width=10, command=lambda: self.toggle_all_mine_reveal(view_mines_button))
        view_mines_button.grid(row=3, column=2)

    def return_to_menu(self, frame):
        frame.after(500, lambda: frame.destroy())
        self.main_menu.after(500, lambda: self.main_menu.pack())


gui = GUI()

mainloop()