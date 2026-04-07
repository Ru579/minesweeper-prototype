from GameManager import GameManager
from tkinter import *
from PIL import Image, ImageTk

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
        self.clock = Label() # either the stopwatch (in Classic) or timer (in Time Trial)

        self.tiles = [] # an array of all Buttons on the cell grid

        # creating logic units
        self.game = GameManager()
        
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
        Button(self.main_menu, image=self.settings_icon, command= lambda: self.create_settings_window()).grid(row=0, column=0)
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
        classic_button_frame.bind("<Button-1>", lambda _: self.start_game("Classic"))
        classic_label.bind("<Button-1>", lambda _: self.start_game("Classic"))
    
    def start_game(self, game_mode):
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

        self.clock = Label(self.game_frame, font=("Calibri", 20), width=5)
        self.clock.grid(row=0, column=2)

        self.cell_grid = Frame(self.game_frame)
        self.cell_grid.grid(row=1, column=1)

        # starting the game
        if game_mode == "Classic":
            self.gui_start_classic_mode()
        elif game_mode == "Time Trial":
            self.gui_start_time_trial()

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
    
    def gui_start_classic_mode(self):
        self.game.start_classic_mode(self.game.main_menu_difficulty)
        self.clock.config(text = "00:00")

        # formatting images
        self.format_images(image_length=60 if self.game.difficulty=="Beginner" else 40)

        # making a 2D array of Buttons- these Buttons will be turned into cells in create_cell_grid()
        self.tiles = [[Button(self.cell_grid) for _ in range(self.game.board.grid_width)] for _ in range(self.game.board.grid_height)]
        
        self.create_cell_grid()

        self.game.user_can_interact = True
    
    def gui_start_time_trial(self):
        self.game.start_time_trial()
        self.clock.config(text = "03:00")

        self.format_images(image_length=62)
        
        self.make_tt_board()
    
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

        # completely removing the old cells and cell
        for widget in self.cell_grid.winfo_children():
            widget.destroy()
        self.cell_grid.destroy()

        # creating a new cell grid and cells
        self.cell_grid = Frame(self.game_frame)
        self.cell_grid.grid(row=1, column=1)
        self.tiles = [[Button(self.cell_grid) for _ in range(self.game.board.grid_width)] for _ in range(self.game.board.grid_height)]
        self.create_cell_grid()

        self.game.user_can_interact = True

    def ui_open_cell(self, row, column):
        pass

    def ui_flag_cell(self, row, column):
        pass

    def ui_confuse_cell(self, row, column):
        pass

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



gui = GUI()
gui.create_main_menu()
mainloop()

