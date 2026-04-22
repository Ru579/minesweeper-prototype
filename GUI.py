from GameManager import GameManager
from LoginGUI import *

class GUI:
    def __init__(self):
        # creating main window
        self.Minesweeper = Tk()
        self.Minesweeper.title("Minesweeper")

        # creating frames
        self.main_menu = Frame(self.Minesweeper)
        self.game_frame = Frame(self.Minesweeper)
        self.game_finished_window = Frame()

        # main menu widgets
        self.difficulty_button = Button()

        # game frame widgets
        self.title = Label()
        self.communicator = Label()
        self.flags_left_counter = Label()
        self.cell_grid = Frame()
        self.clock = Label() # either the stopwatch (in Classic) or timer (in Time Trial)

        # game over widgets
        self.return_to_game_over_button = Button()
        self.view_mines_button = Button()

        self.tiles = [] # an array of all Buttons on the cell grid

        # creating logic units
        self.game = GameManager()
        # creating GUI logic units
        self.loginGUI = LoginGUI(self.game.database, self.Minesweeper)
        
        # PREPARING IMAGES

        # CELL IMAGES
        # cell images are the images as they appear in the folder, not resized or formatted
        self.cell_images = {
            "hidden_cell_image": Image.open("Images/hidden_cell.png"),
            "mine_image": Image.open("Images/mine_cell_red.png"),
            "flagged_cell_image": Image.open("Images/minesweeper_flag.png"),
            "incorrect_flagged_image": Image.open("Images/incorrect_flag.png"),
            "confused_cell_image": Image.open("Images/confused_cell_v3_green.png"),
            "highlighted_hidden_cell_image": Image.open("Images/highlighted_hidden_cell.png"),
            "highlighted_flagged_cell_image": Image.open("Images/highlighted_minesweeper_flag.png"),
            "highlighted_confused_cell_image": Image.open("Images/highlighted_confused_cell_v3_green.png")
        }
        self.formatted_cell_images = {}
        # cell number images are the images of cells with numbers as they appear in the folder, not resized or formatted
        self.cell_number_images = []
        for i in range(9):
            current_image = Image.open(f"Images/{i}_cell.png")
            self.cell_number_images.append(current_image)
        self.formatted_number_images = []

        # settings icon
        settings_icon = Image.open("Images/settings_icon.jpg")
        self.settings_icon = ImageTk.PhotoImage(settings_icon.resize((60,60)))
        # account icon
        guest_icon = Image.open("Images/guest_profile.png")
        self.guest_icon = ImageTk.PhotoImage(guest_icon.resize((60,60)))
        # clock icon
        clock_icon = Image.open("Images/clock_symbol_v2.png")
        self.clock_icon = ImageTk.PhotoImage(clock_icon.resize((60,60)))
        # flag counter icon
        flag_counter_icon = Image.open("Images/minesweeper_flag.png")
        self.flag_counter_icon = ImageTk.PhotoImage(flag_counter_icon.resize((60,60)))

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
        # settings button
        settings_button = Label(self.main_menu, image=self.settings_icon)
        settings_button.bind("<Button-1>", lambda _: self.create_settings_window())
        settings_button.grid(row=0, column=0)
        # account button
        self.loginGUI.create_profile(self.main_menu)

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
        classic_button_frame.bind("<Button-1>", lambda _: self.start_game("Classic"))
        classic_label.bind("<Button-1>", lambda _: self.start_game("Classic"))
    
    def start_game(self, game_mode, difficulty=""):
        # swapping frames
        self.main_menu.forget()
        self.game_frame = Frame(self.Minesweeper)
        self.game_frame.pack()

        # creating the game frame widgets
        # title
        self.game_frame_title = Label(self.game_frame, font=("Calibri Bold", 30))
        self.game_frame_title.grid(row=0, column=2)
        # textbox at bottom of screen
        self.communicator = Label(self.game_frame, text="Click a cell to start", font=("Calibri", 18), width=24, wraplength=300, height=2)
        self.communicator.grid(row=3, column=2, rowspan=4)
        
        # making flag counter
        self.flag_counter = Label(self.game_frame, text="", font=("Calibri", 20), width=2)
        self.flag_counter.grid(row=1, column=1)
        Label(self.game_frame, image=self.flag_counter_icon, bg="white").grid(row=1, column=0) # flag counter icon

        # making clock icon
        self.clock = Label(self.game_frame, font=("Calibri", 20), width=5)
        self.clock.grid(row=1, column=3)
        Label(self.game_frame, image=self.clock_icon).grid(row=1, column=4) # clock icon

        # Return to menu button
        Button(self.game_frame, text="Menu", bg="black", fg="white", font=("Calibri Bold", 14),
               command=lambda: self.return_to_menu_attempt()).grid(row=0, column=0)

        self.cell_grid = Frame(self.game_frame)
        self.cell_grid.grid(row=2, column=2)

        # starting the game
        if game_mode == "Classic":
            if difficulty: # a difficulty is only passed in if retrying in Classic mode
                self.gui_start_classic_mode(difficulty)
            else: # otherwise, if starting Classic mode from main menu, use that difficulty
                self.gui_start_classic_mode(self.game.main_menu_difficulty)
        elif game_mode == "Time Trial":
            self.gui_start_time_trial()

        # updating number of flags left after starting correct game mode
        self.flag_counter.config(text = str(self.game.board.flags_left))
    
    def return_to_menu_attempt(self):        
        self.game.timer_on = False # pausing the timer whilst the popup is up
        
        if (self.game.board_started and self.game.game_mode == "Classic") or self.game.tt_running: # if a game is running
            self.cell_grid.grid_forget() # hiding cell grid whilst the popup is up

            # creating and displaying popup
            warning_popup = Toplevel()
            warning_popup.title("UNSAVED GAME")
            Label(warning_popup, font=("Calibri", 16),
                  text="Are you sure you want to return to the main menu?\nYour progress in this game WON'T be saved.").pack()
            Button(warning_popup, text="Quit to Menu", font=("Calibri Bold", 16), bg="red",
                   command=lambda:self.return_to_menu(self.game_frame, warning_popup)).pack()
            Button(warning_popup, text="Return to Game", font=("Calibri", 16),
                   command=lambda:self.return_to_game_from_warning(warning_popup)).pack()
            
            # making the player only able to click on the popup window until it is closed
            warning_popup.transient(self.Minesweeper) # keeps popup on top of game_frame
            warning_popup.grab_set() # stops interactions with game_frame
            self.Minesweeper.wait_window(warning_popup) # preventing following lines from being executed until popup closed
            self.cell_grid.grid(row=2, column=2)
            if self.game.board_started:
                self.game.timer_on = True
        
        else: # if returning to menu before first click or when viewing board after game completion
            self.game_finished_window.destroy()
            self.return_to_menu(self.game_frame)

    def return_to_game_from_warning(self, popup_window):
        popup_window.destroy()
        if self.game.board_started:
            self.game.timer_on = True
        self.cell_grid.grid(row=2, column=2)

    def change_difficulty(self):
        new_difficulty = self.game.difficulty_mapper[self.difficulty_button.cget("text")]
        self.difficulty_button.config(text = new_difficulty)
        self.game.main_menu_difficulty = new_difficulty
    
    def create_settings_window(self):
        pass

    def account_interaction(self):
        pass
    
    def gui_start_classic_mode(self, difficulty):
        self.game.start_classic_mode(difficulty)
        self.game_frame_title.config(text="CLASSIC MODE")
        self.clock.config(text = "00:00")

        # formatting images
        self.format_images(image_length=62 if self.game.difficulty=="Beginner" else 42)

        # making a 2D array of Buttons- these Buttons will be turned into cells in create_cell_grid()
        self.tiles = [[Button(self.cell_grid) for _ in range(self.game.board.grid_width)] for _ in range(self.game.board.grid_height)]
        
        self.create_cell_grid()

        self.game.user_can_interact = True
    
    def gui_start_time_trial(self):
        self.game.start_time_trial()
        self.game_frame_title.config(text="TIME TRIAL")
        self.clock.config(text = "03:00")

        self.format_images(image_length=62)
        
        self.make_tt_board()
    
    def format_images(self, image_length):
        # clearing old sizes applied to cell images
        if self.formatted_number_images:
            self.formatted_number_images = []
        
        # resizing each image
        for image in self.cell_images:
            self.formatted_cell_images[image] = self.cell_images[image].resize((image_length, image_length))
            self.formatted_cell_images[image] = ImageTk.PhotoImage(self.formatted_cell_images[image])
        for number in range(9):
            temp_number_image = self.cell_number_images[number].resize((image_length, image_length))
            temp_number_image = ImageTk.PhotoImage(temp_number_image)
            self.formatted_number_images.append(temp_number_image)
    
    def create_cell_grid(self):
        for i in range(0, self.game.board.grid_height):
            for j in range(0, self.game.board.grid_width):
                # creating a new button with a left-click command
                tile = Button(self.cell_grid, command = lambda row=i, column=j: self.ui_open_cell(row, column))
                # adding middle and right click commands
                tile.bind("<Button-2>", lambda _, row=i, column=j: self.ui_confuse_cell(row, column))
                tile.bind("<Button-3>", lambda _, row=i, column=j: self.ui_flag_cell(row, column))

                # applying cell images
                tile.config(image=self.formatted_cell_images["hidden_cell_image"])

                # resizing cells
                if self.game.difficulty == "Beginner" or self.game.tt_difficulty in ("Easy", "Medium"):
                    tile.config(width=60, height=60)
                elif self.game.difficulty in ("Intermediate", "Expert") or self.game.tt_difficulty in ("Hard", "Very Hard"):
                    tile.config(width=40, height=40)

                tile.grid(row=i, column=j)
                # adding this button to a 2D array so that it can be accessed later
                self.tiles[i][j] = tile
    
    def make_tt_board(self):
        # setting board_started to False in preparation for player opening the first cell on the new board
        self.game.board_started = False
        self.flag_counter.config(text=str(self.game.board.flags_left))

        # completely removing the old cells and cell
        for widget in self.cell_grid.winfo_children():
            widget.destroy()
        self.cell_grid.destroy()

        # creating a new cell grid and cells
        self.cell_grid = Frame(self.game_frame)
        self.cell_grid.grid(row=2, column=2)
        self.tiles = [[Button(self.cell_grid) for _ in range(self.game.board.grid_width)] for _ in range(self.game.board.grid_height)]
        self.create_cell_grid()

        self.game.user_can_interact = True

    def ui_open_cell(self, x, y):
        if self.game.user_can_interact:
            self.game.open_cell(x, y)
            self.update_ui()
            self.communicator.config(text="") # hiding previous communicator text

            # if game hasn't started yet, starts the respective timers
            if not self.game.board_started:
                self.game.board_started = True
                if self.game.game_mode == "Classic":
                    self.clock.after(1000, lambda: self.update_countup_timer(0, 0))
                elif self.game.game_mode == "Time Trial" and not self.game.tt_running:
                    self.clock.after(1000, lambda: self.gui_update_countdown_timer())
                    self.game.tt_running = True
            
            # unssuccessful chord
            if self.game.board.chording_enabled and self.game.board.flag_difference != 0:
                # iterating through surrounding cells
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if self.game.board.in_bounds(i, j):
                            state = self.game.get_cell(i, j, "state")
                            
                            # if player has placed too few flags, meaning we highlight surrounding hidden or confused cells
                            if self.game.board.flag_difference < 0 and state in ("Hidden", "Confused"):
                                self.tiles[i][j].config(image=self.formatted_cell_images[f"highlighted_{state.lower()}_cell_image"])

                            # if player has placed too many flags, meaning we highlight surrounding flagged cells
                            if self.game.board.flag_difference > 0 and state == "Flagged":
                                self.tiles[i][j].config(image=self.formatted_cell_images["highlighted_flagged_cell_image"])
                            
                            # restoring the cell to its original image after 500ms
                            self.tiles[i][j].after(500, lambda row=i, column=j, current_state=state: self.fix_cell_colour(row, column, old_state= current_state))
                
                # reporting flag difference
                self.communicator.config(text=f"Cell has {abs(self.game.board.flag_difference)} too {"many" if self.game.board.flag_difference>0 else "few"} flags")
            
            self.game_state_check()

    def ui_flag_cell(self, x, y):
        if self.game.user_can_interact:
            self.game.board.flag_cell(x, y)

            # if a cell is being flagged
            if self.game.get_cell(x, y, "state") == "Flagged":
                self.tiles[x][y].config(image=self.formatted_cell_images["flagged_cell_image"])
            # if a cell is being unflagged
            elif self.game.get_cell(x, y, "state") == "Hidden":
                self.tiles[x][y].config(image=self.formatted_cell_images["hidden_cell_image"])

            # if the player has ran out of flags
            if self.game.board.not_enough_flags:
                self.communicator.config(text="Not enough flags")
                self.communicator.after(500, lambda: self.communicator.config(text=""))
                self.game.board.not_enough_flags = False
            
            # updating flag counter
            self.flag_counter.config(text=str(self.game.board.flags_left))

    def ui_confuse_cell(self, x, y):
        if self.game.user_can_interact:
            self.game.board.confuse_cell(x, y)

            state = self.game.get_cell(x, y, "state")
            # making cell image reflect new state after confusing/un-confusing
            if state in ("Hidden", "Confused"):
                self.tiles[x][y].config(image=self.formatted_cell_images[f"{state.lower()}_cell_image"])

            # updating flag counter
            self.flag_counter.config(text=str(self.game.board.flags_left))

    def update_ui(self):
        # iterating through each cell on the board and updating images of revealed cells
        for i in range(self.game.board.grid_height):
            for j in range(self.game.board.grid_width):
                if self.game.get_cell(i, j, "state") == "Revealed":
                    if self.game.get_cell(i, j, "value") == "*": # if cell is a mine
                        self.tiles[i][j].config(image=self.formatted_cell_images["mine_image"])
                    else: # showing the number on the cell
                        self.tiles[i][j].config(image=self.formatted_number_images[int(self.game.get_cell(i, j, "value"))])

    def fix_cell_colour(self, x, y, old_state):
        # old_state is equal to the state of the Cell at (x, y) BEFOPRE highlighting occurred
        new_state = self.game.get_cell(x, y, "state") # new_state is the state of the cell at (x, y) AFTER highlighting has occurred
        if old_state == new_state and old_state != "Revealed":
           self.tiles[x][y].config(image=self.formatted_cell_images[f"{old_state.lower()}_cell_image"])

    def update_countup_timer(self, minutes, seconds):
        if self.game.timer_on:
            # incrementing timer
            seconds += 1
            self.game.stopwatch += 1
            if seconds == 60:
                seconds = 0
                minutes += 1
            self.clock.config(text=f"{minutes:02}:{seconds:02}")
            self.clock.after(1000, lambda: self.update_countup_timer(minutes, seconds)) # incrementing the timer again after 1 second
        
        elif self.game.board_started: # if gameplay is currently paused due to return to menu attempt
            # checking every 200ms for when the timer becomes on again
            self.clock.after(200, lambda: self.update_countup_timer(minutes, seconds))

    def gui_update_countdown_timer(self):
        self.game.update_countdown_timer()
        if self.game.time_change_type == "Time Added" or self.game.time_change_type == "Time Normal":
            # updating the timer as normal
            self.clock.config(text=f"{self.game.minutes:02}:{self.game.seconds:02}")
            self.clock.after(1000, lambda: self.gui_update_countdown_timer())
        elif self.game.time_change_type == "Time Game Over":
            self.clock.config(text="00:00")
            self.do_game_over()
        elif self.game.tt_running: # checking every 200ms for when the timer becomes on again
            self.clock.after(200, lambda: self.gui_update_countdown_timer())
    
    def game_state_check(self):
        if self.game.board.game_over: # if a mine has been revealed
            self.do_game_over()
        
        elif self.game.game_mode == "Classic":
            if self.game.game_won: # ending the game and showing the appropriate game over screen
                self.game.terminate_game_variables()
                self.game.update_game_data(outcome="Win")

                self.communicator.config(text="Congratulations!")

                self.game_frame.after(500, lambda: self.prepare_game_finished_window("Win"))


        elif self.game.game_mode == "Time Trial":
            if self.game.board_done:  # progressing onto the next stage in Time Trial if current one is completed
                self.game.timer_on = False
                self.communicator.config(text="Next Stage")
                self.ui_next_tt_stage()
    
    def do_game_over(self, delay=1250):
        # stopping all attributes that cause the game to continue
        self.game.tt_running = False
        self.game.board_started = False
        self.game.timer_on = False

        # if player ran out of time in Time Trial
        if self.game.time_change_type == "Time Game Over":
            self.game.terminate_game_variables()
            self.game.update_game_data(outcome="Lose", mine_clicked=False)
            self.communicator.config(text="GAME OVER: Time Ran Out!")
        
        # if player clicked mine in Classic or Time Trial
        else:
            self.game.terminate_game_variables()
            self.game.update_game_data(outcome="Lose", mine_clicked=True)
            self.communicator.config(text="GAME OVER!")
            self.toggle_all_mine_reveal(button_used=False)
        
        self.game_frame.after(delay, lambda: self.prepare_game_finished_window("Lose"))
    
    def ui_next_tt_stage(self):
        self.communicator.config(text="Next Stage")
        self.game.time_to_be_added = True
        self.game.terminate_game_variables()
        # making next board
        self.game.next_tt_stage()
        self.game_frame.after(500, lambda: self.make_tt_board())

    def prepare_game_finished_window(self, outcome):
        # swapping frames to game finished window
        self.game_frame.forget()
        self.game_finished_window = Frame(self.Minesweeper)
        self.game_finished_window.pack()
        
        # creating the respective game over window
        if self.game.game_mode == "Classic":
            self.display_classic_game_over_window(outcome)
        elif self.game.game_mode == "Time Trial":
            self.display_tt_game_over_window()
    
    def display_classic_game_over_window(self, outcome):
        # creates text confirming outcome and final time
        if outcome == "Win":
            Label(self.game_finished_window,
                  text=self.game.calculate_output_statement(current_communicator_text=""),
                  font=("Calibri", 16)).grid(row=0, column=1)
        elif outcome == "Lose":
            Label(self.game_finished_window,
                  text=self.game.calculate_output_statement(current_communicator_text=""),
                  font=("Calibri", 16)).grid(row=0, column=1)
        
        # creating grid of buttons to interact with after game is over: retry, change difficulty etc.
        game_finished_options = Frame(self.game_finished_window)
        game_finished_options.grid(row=1, column=1)

        # making difficulty changer button
        retry_difficulty_changer = Button(game_finished_options, text="Change Difficulty?", bg="green", fg="white", font=("Calibri", 16), width=15,
                                          command=lambda: self.change_retry_difficulty(retry_difficulty_changer))
        retry_difficulty_changer.grid(row=0, column=1)
        # making the retry button
        retry_button = Button(game_finished_options, text="Retry?", bg="blue", fg="white", font=("Calibri", 16), width=15,
                              command=lambda: self.retry(label_to_check=retry_difficulty_changer, destroy_game_over_window=True))
        retry_button.grid(row=0, column=0)
        # View board button
        Button(game_finished_options, text="View Board?", font=("Calibri", 16), width=15,
               command=lambda: self.view_board()).grid(row=1, column=0)
        # return to menu button
        Button(game_finished_options, text="Menu", font=("Calibri", 16), width=15,
               command=lambda: self.return_to_menu(self.game_finished_window)).grid(row=1, column=1)

    def display_tt_game_over_window(self):
        # making label outlining final score
        Label(self.game_finished_window,
              text=self.game.calculate_output_statement(current_communicator_text=""),
              font=("Calibri", 16)).grid(row=0, column=1)

        # making retry button
        retry_button = Button(self.game_finished_window, text="Retry?", bg="blue", fg="white", font=("Calibri", 15), width=6,
                              command=lambda: self.retry(destroy_game_over_window=True))
        retry_button.grid(row=1, column=1)

        # view board and return to menu buttons
        Button(self.game_finished_window, text="View Board?", font=("Calibri", 16), command=lambda: self.view_board()).grid(row=2, column=1)
        Button(self.game_finished_window, text="Menu", font=("Calibri", 16),
               command=lambda: self.return_to_menu(self.game_finished_window)).grid(row=3, column=1)

    def retry(self, label_to_check = None, destroy_game_over_window=False):
        if self.game.game_mode == "Classic":
            # retries at the current difficulty unless the player has changed the difficulty they wish to play
            if label_to_check.cget("text") == "Change Difficulty?": # difficulty not changed if text is still the default
                difficulty = self.game.difficulty
            else:
                difficulty = label_to_check.cget("text")
                
            self.game_frame.destroy()
            self.start_game("Classic", difficulty)
        
        elif self.game.game_mode == "Time Trial":
            self.game_frame.destroy()
            self.start_game("Time Trial")
        
        # if retrying from game_finished_window, that window will be destroyed
        if destroy_game_over_window:
            self.game_finished_window.destroy()

    def change_retry_difficulty(self, difficulty_button):
        # creating the popup menu with the three difficulties- selecting a difficulty sets the button's text to that value
        difficulties_menu = Menu(self.game_frame, tearoff=False)
        for difficulty in "Beginner", "Intermediate", "Expert":
            difficulties_menu.add_command(label=difficulty,
                                          command=lambda current_difficulty=difficulty: difficulty_button.config(text=current_difficulty))
        # showing the popup menu
        try:
            x = difficulty_button.winfo_rootx()
            y = difficulty_button.winfo_rooty()
            difficulties_menu.tk_popup(x, y)
        finally:
            difficulties_menu.grab_release()

    def view_board(self):
        # swapping frames back to the grid of cells
        self.game_finished_window.forget()
        self.game_frame.pack()
        
        # revealing mines if not already done in Time Trial due to Time Game Over
        if self.game.game_mode == "Time Trial" and self.game.time_change_type == "Time Game Over":
            self.toggle_all_mine_reveal(button_used=False)

        # removing old buttons (with possible incorrect text)
        self.return_to_game_over_button.destroy()
        self.view_mines_button.destroy()

        # placing new buttons in game frame
        self.return_to_game_over_button = Button(self.game_frame, text="Back to Game Over Screen", bg="blue", fg="white", font=("Calibri", 15),
                                                 width=15, wraplength=150, command=lambda: self.return_to_game_over_screen())
        self.return_to_game_over_button.grid(row=3, column=4)
        self.view_mines_button = Button(self.game_frame, text="Hide Mines" if self.game.mines_revealed else "View Mines", bg="yellow",
                                        font=("Calibri", 15), width=10, command=lambda: self.toggle_all_mine_reveal(button_used=True))
        self.view_mines_button.grid(row=4, column=4)

    def return_to_menu(self, frame, frame2=None):
        frame.after(500, lambda: frame.destroy())
        if frame2:
            frame2.after(500, lambda: frame2.destroy())
        self.main_menu.after(500, lambda: self.main_menu.pack())
    
    def return_to_game_over_screen(self):
        self.game_frame.forget()
        self.game_finished_window.pack()

    def toggle_all_mine_reveal(self, button_used):
        # reveal all cells that are mines and adjust flag images
        if not self.game.mines_revealed or not button_used:
            for i in range(self.game.board.grid_height):
                for j in range(self.game.board.grid_width):
                    value = self.game.get_cell(i, j, "value")
                    state = self.game.get_cell(i, j, "state")
                    if value == "*" and state != "Flagged": # is a mine that was not identified and flagged by player
                        self.tiles[i][j].config(image=self.formatted_cell_images["mine_image"])
                    elif value != "*" and state == "Flagged": # is a non-mine cell that was incorrectly flagged
                        self.tiles[i][j].config(image=self.formatted_cell_images["incorrect_flagged_image"])
            
            if button_used: # if the View Mines button is being used to reveal mines
                self.view_mines_button.config(text="Hide Mines")
            self.game.mines_revealed = True
        
        # hide all mines and restore flag images
        else:
            for i in range(self.game.board.grid_height):
                for j in range(self.game.board.grid_width):
                    value = self.game.get_cell(i, j, "value")
                    state = self.game.get_cell(i, j, "state")
                    if state == "Confused": # if a cell is confused, show it to be so (if changed by mines being revealed)
                        self.tiles[i][j].config(image=self.formatted_cell_images["confused_cell_image"])
                    elif value != "*" and state == "Flagged": # a cell has been shown to have been incorrectly flagged
                        self.tiles[i][j].config(image=self.formatted_cell_images["flagged_cell_image"])
                    elif value == "*" and state != "Flagged": # a cell was a mine but was not flagged 
                        self.tiles[i][j].config(image=self.formatted_cell_images["hidden_cell_image"])
            
            self.view_mines_button.config(text="View Mines")
            self.game.mines_revealed = False



gui = GUI()
gui.create_main_menu()
mainloop()

