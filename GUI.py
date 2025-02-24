from GameManager import *
# from Widget import *
from Settings import *
#from Tester import Minesweeper


# from tkinter import *
# from PIL import Image, ImageTk


def ui_open_cell(x, y):
    game.open_cell(x, y)
    update_ui()
    widgets.communicator.config(text="")
    if not game.game_started:
        game.game_started = True
        if game.game_mode == "Classic":
            widgets.countup_timer.after(1000, lambda: update_countup_timer(0, 0))
        if game.game_mode == "Time Trial" and not game.tt_running:
            game.tt_running = True
            widgets.countdown_timer.after(1000, lambda: update_countdown_timer(3, 0))

    if game.flag_difference < 0:
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if game.board.in_bounds(i, j) and game.get_cell(i, j, "state") == "Hidden":
                    tiles[i][j].config(bg="purple")
                    return_cell_to_normal(i,j,"#d8d8d8")
                    #tiles[i][j].after(500, lambda row=i, column=j: tiles[row][column].config(bg="#d8d8d8"))
        widgets.communicator.config(text=f"Cell has {-1 * game.flag_difference} too few flags.")
    if game.flag_difference > 0:
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if game.board.in_bounds(i, j) and game.get_cell(i, j, "state") == "Flagged":
                    tiles[i][j].config(bg="purple")
                    return_cell_to_normal(i,j,"blue")
                    #tiles[i][j].after(500, lambda row=i, column=j: tiles[row][column].config(bg="blue"))
        widgets.communicator.config(text=f"Cell has {game.flag_difference} too many flags.")

    game_state_check()


def return_cell_to_normal(row,column, colour):
    tiles[row][column].after(500,lambda x=row, y=column: fix_cell_colour(x,y, colour))


def fix_cell_colour(row,column, colour):
    state = game.get_cell(row, column, "state")
    if colour=="#d8d8d8" and state=="Hidden":
        tiles[row][column].config(bg=colour)
    elif colour=="blue" and state=="Flagged":
        tiles[row][column].config(bg=colour)


def ui_flag_cell(x, y):
    game.flag_cell(x, y)
    if game.get_cell(x, y, "state") == "Flagged":
        tiles[x][y].config(bg="blue", text="")
    elif game.get_cell(x, y, "state") == "Hidden":
        tiles[x][y].config(bg="#d8d8d8", text="")
        if game.board.not_enough_flags:
            widgets.communicator.config(text="Not enough flags")
            widgets.communicator.after(500, lambda: widgets.communicator.config(text=""))
            game.board.not_enough_flags = False
    widgets.mines_left_counter.config(text=str(game.mines_left))


def ui_confuse_cell(x, y):
    game.confuse_cell(x, y)
    if game.get_cell(x, y, "state") == "Confused":
        tiles[x][y].config(bg="green", text="?")
    if game.get_cell(x, y, "state") == "Hidden":
        tiles[x][y].config(bg="#d8d8d8", text="")
    widgets.mines_left_counter.config(text=str(game.mines_left))


def update_ui():
    for i in range(0, game.board.grid_height):
        for j in range(0, game.board.grid_width):
            if game.get_cell(i, j, "state") == "Revealed":
                tiles[i][j].config(text=game.board.grid[i][j].value, bg="white")
                if game.get_cell(i, j, "value") == "*":
                    tiles[i][j].config(bg="red")

                    # global image
                    # image=PhotoImage(file="Minesweeper_flag_v4.png")
                    # image = image.resize(10,10)
                    # tiles[i][j].config(image=image)
                    # tiles[i][j].config(image=PhotoImage(file="Minesweeper_flag.png"))
                    # img = PhotoImage(img0)
                    # tiles[i][j].config(img)
                if game.get_cell(i, j, "value") == "0":
                    tiles[i][j].config(text="")


def update_countup_timer(minutes, seconds):
    if game.timer_on:
        seconds += 1
        if seconds == 60:
            seconds = 0
            minutes += 1
        widgets.countup_timer.config(text=f"{minutes:02}:{seconds:02}")
        widgets.countup_timer.after(1000, lambda: update_countup_timer(minutes, seconds))


def update_countdown_timer(minutes, seconds):
    game.time_change_type = ""
    minutes, seconds = game.update_countdown_timer(minutes, seconds)
    if game.time_change_type == "Time Added" or game.time_change_type == "Time Normal":
        widgets.countdown_timer.config(text=f"{minutes:02}:{seconds:02}")
        widgets.countdown_timer.after(1000, lambda: update_countdown_timer(minutes, seconds))
    elif game.time_change_type == "Time Game Over":
        widgets.countdown_timer.config(text="00:00")
        finish_board()
        do_game_over(1800)
    elif game.tt_running:
        widgets.countdown_timer.after(200, lambda: update_countdown_timer(minutes, seconds))


def change_difficulty(difficulty):
    if difficulty == "Beginner":
        difficulty_button.config(text="Intermediate")
    elif difficulty == "Intermediate":
        difficulty_button.config(text="Expert")
    elif difficulty == "Expert":
        difficulty_button.config(text="Beginner")


def game_state_check():
    if game.board.game_over:
        game.tt_running = False
        finish_board()
        do_game_over()
        game.game_started = False
    elif game.game_mode == "Classic":
        if game.game_has_been_won:
            #not 100% sure about the following line
            game.timer_on = False

            finish_board()
            widgets.communicator.config(text="Congratulations!")
            game.game_started = False
            if settings.user_settings["create_game_finished_window"]:
                game_frame.after(500, lambda: create_game_finished_window("WIN"))
            else:
                make_quick_replay_buttons()

    elif game.game_mode == "Time Trial":
        if game.board_done:
            game.timer_on=False # stops timer from ticking down when swapping stages (I think)
            widgets.communicator.config(text="Next Stage")
            next_tt_stage()


def next_tt_stage():
    finish_board()
    widgets.communicator.config(text="Next Stage")
    game.time_to_be_added = True
    # widgets.countdown_timer.config(text=game.add_time(widgets.countdown_timer.cget("text")))
    game.next_tt_stage()
    game.timer_on = False
    widgets.mines_left_counter.config(text=game.mines_left)
    game_frame.after(500, lambda: make_tt_board())
    #game.timer_on = True

    #SHOULD BE SET TO FALSE??



def finish_board():
    for i in range(0, game.board.grid_height):
        for j in range(0, game.board.grid_width):
            tiles[i][j].config(state=DISABLED)


def do_game_over(delay=1250):
    game.timer_on=False
    if game.game_mode == "Time Trial" and widgets.countdown_timer.cget("text") == "00:00":
        widgets.communicator.config(text="GAME OVER: Time Ran Out!")
        if not settings.user_settings["create_game_finished_window"]:
            view_mines_button = Button(game_frame, bg="yellow", text="View Mines", font=("Calibri", 15), width=10, command=lambda: reveal_all_mines(view_mines_button))
            view_mines_button.grid(row=3,column=2)
    else:
        widgets.communicator.config(text="GAME OVER!")
        reveal_all_mines()

    if settings.user_settings["create_game_finished_window"]:
        game_frame.after(delay, lambda: create_game_finished_window("LOSE"))
    else:
        make_quick_replay_buttons()
        #code for make_quick_replay_buttons


def reveal_all_mines(button=None):
    if not game.mines_revealed:
        for i in range(game.board.grid_height):
            for j in range(game.board.grid_width):
                if game.get_cell(i,j,"value")=="*":
                    tiles[i][j].config(text="*", bg="red")
                    if game.get_cell(i,j,"state")=="Flagged":
                        tiles[i][j].config(text="*/F", bg="purple")
                elif game.get_cell(i,j,"state")=="Flagged": #is a flagged cell and was not a mine (the previous if statement's condition was not met)
                    tiles[i][j].config(fg="red", text="X")
        #if game.game_mode == "Time Trial" and widgets.countdown_timer.cget("text") == "00:00":
        if button is not None:
            button.config(text="Hide Mines")
        game.mines_revealed=True
    else:
        for i in range(game.board.grid_height):
            for j in range(game.board.grid_width):
                if tiles[i][j].cget("text")=="*/F" or tiles[i][j].cget("text")=="X":
                    tiles[i][j].config(text="", bg="blue")
                elif tiles[i][j].cget("text")=="*":
                    tiles[i][j].config(text="", bg="#d8d8d8")
        button.config(text="View Mines")
        game.mines_revealed=False


def make_quick_replay_buttons():
    #game.timer_on = False
    retry_button = Button(game_frame, text="Retry?", bg="blue", fg="white", font=15, width=10)  # command=lambda: retry(game.game_mode))
    retry_button.grid(row=2, column=0)
    Button(game_frame, text="Menu", bg="blue", fg="white", font=15, width=10, command=lambda: return_to_menu(game_frame)).grid(row=2, column=2)
    if game.game_mode == "Classic":
        difficulty_changer = Label(game_frame, text="Change Difficulty?", bg="green", fg="white", font=15, width=15)
        difficulty_changer.bind("<Button-1>", lambda event: change_retry_difficulty(difficulty_changer))
        difficulty_changer.grid(row=3, column=0)
        retry_button.bind("<Button-1>", lambda event: retry(game.game_mode, difficulty_changer))
    else:
        retry_button.bind("<Button-1>", lambda event: retry(game.game_mode))
        Label(game_frame, text=f"Stage: {game.stage-5}\nYou lasted for- {game.stopwatch//60:02}:{game.stopwatch%60:02}", font=("Calibri Bold", 15), bg="dark grey", fg="green").grid(row=3, column=1)


def change_retry_difficulty(button):
    difficulties = Menu(game_frame, tearoff=False)
    difficulties.add_command(label="Beginner", command=lambda: button.config(text="Beginner"))
    difficulties.add_command(label="Intermediate", command=lambda: button.config(text="Intermediate"))
    difficulties.add_command(label="Expert", command=lambda: button.config(text="Expert"))
    try:
        x = button.winfo_rootx()
        y = button.winfo_rooty()
        difficulties.tk_popup(x, y)
    finally:
        difficulties.grab_release()


#def retry(a,b):
#    pass

def retry(game_mode, label=None, destroy_window=False):
    if game.game_mode == "Classic":
        text = label.cget("text")
        if text == "Change Difficulty?":
            difficulty = game.difficulty
        else:
            difficulty = text
        game_frame.destroy()
        start_game(game_mode, difficulty)

    else:
        game_frame.destroy()
        start_game(game_mode)
    if destroy_window:
        game_finished_window.destroy()


def create_game_finished_window(outcome):
    final_time = []
    if game.game_mode == "Classic":
        final_time = [widgets.countup_timer.cget("text")[0:2], widgets.countup_timer.cget("text")[3:5]]
    elif game.game_mode == "Time Trial":
        final_time = [f"{game.stopwatch // 60:02}", f"{game.stopwatch % 60:02}"]
    game.timer_on = False
    game_frame.forget()
    global game_finished_window
    game_finished_window = Frame(Minesweeper)
    game_finished_window.pack()
    for i in range(4):
        game_finished_window.columnconfigure(i, weight=1)
        if i == 0 or i == 3:
            game_finished_window.rowconfigure(i, weight=3)
        elif i == 1 or i == 2:
            game_finished_window.rowconfigure(i, weight=2)
    game_finished_window.rowconfigure(0, weight=3)
    if game.game_mode == "Classic":
        classic_game_over_window(outcome, final_time)
    elif game.game_mode == "Time Trial":
        tt_game_over_window(final_time)


def classic_game_over_window(outcome, final_time):
    if outcome == "WIN":
        Label(game_finished_window, text=f"Your time was:\n {final_time[0]}:{final_time[1]}", font=("Calibri", 16)).grid(row=0, column=1)
        #Label(game_finished_window, text=f"Your time was:\n {final_time[0]}:{final_time[1]}\nPlease enter your username below", font=("Calibri", 16)).grid(row=0, column=1)
        #username = Entry(game_finished_window, font=("Calibri", 16))
        #username.grid(row=1, column=1)
        #Button(game_finished_window, text="CONFIRM", font=("Calibri", 16), command=lambda: user_info_get(username.get(), final_time)).grid(row=2, column=1)
    elif outcome == "LOSE":
        Label(game_finished_window, text=f"GAME OVER!\nYour time was {final_time[0]}:{final_time[1]}", font=("Calibri", 16)).grid(row=0, column=1)

    game_finished_options = Frame(game_finished_window)
    retry_button = Button(game_finished_options, text="Retry?", bg="blue", fg="white", font=("Calibri", 16), width=15, command=lambda: retry(game.game_mode, difficulty_changer, destroy_window=True))
    retry_button.grid(row=0, column=0)
    difficulty_changer = Button(game_finished_options, text="Change Difficulty?", bg="green", fg="white", font=("Calibri", 16), width=15)
    difficulty_changer.bind("<Button-1>", lambda event: change_retry_difficulty(difficulty_changer))
    difficulty_changer.grid(row=0, column=1)
    Button(game_finished_options, text="View Board?", font=("Calibri", 16), width=15, command=lambda: view_board()).grid(row=1, column=0)
    Button(game_finished_options, text="Close", font=("Calibri", 16), width=15, command=lambda: return_to_menu(game_finished_window)).grid(row=1, column=1)
    game_finished_options.grid(row=1, column=1)


def tt_game_over_window(final_time):
    Label(game_finished_window, text=f"You got to stage {game.stage - 5}\nYou lasted for:\n {game.stopwatch // 60:02}:{game.stopwatch % 60:02}", font=("Calibri", 16)).grid(row=0, column=1)
    retry_button = Button(game_finished_window, text="Retry?", bg="blue", fg="white", font=15, width=6, command=lambda: retry(game.game_mode, destroy_window=True))
    retry_button.grid(row=1, column=1)
    Button(game_finished_window, text="View Board?", font=("Calibri", 16), command=lambda: view_board()).grid(row=2, column=1)
    Button(game_finished_window, text="Close", font=("Calibri", 16), command=lambda: return_to_menu(game_finished_window)).grid(row=3, column=1)



    #Label(game_finished_window, text=f"You lasted for:\n {game.stopwatch // 60:02}:{game.stopwatch % 60:02}\nPlease enter your username below", font=("Calibri", 16)).grid(row=0, column=1)
    #username = Entry(game_finished_window, font=("Calibri", 16))
    #username.grid(row=1, column=1)
    #confirm_button = Button(game_finished_window, text="CONFIRM NAME", font=("Calibri", 16), command=lambda: name_confirm(confirm_button, username.get(), final_time))
    #confirm_button.grid(row=2, column=1)


def name_confirm(button, username, time):
    user_info_get(username, time)
    button.destroy()
    Button(game_finished_window, text="View Board?", font=("Calibri", 16), command=lambda: view_board()).grid(row=2, column=0)
    Button(game_finished_window, text="MENU", font=("Calibri", 16), command=lambda: return_to_menu(game_finished_window)).grid(row=2, column=2)


def user_info_get(username, time):  # where time is an array, 1st index is minutes, 2nd index is seconds
    if game.game_mode == "Classic":
        add_classic_user_info(username, time)
        return_to_menu(game_finished_window)
    if game.game_mode == "Time Trial":
        add_tt_user_info(username, time)


def return_to_menu(frame):
    frame.after(500, lambda: frame.destroy())
    main_menu.after(500, lambda: main_menu.pack())


#use reveal all mines function if in time trial and countdown timer = "00:00", because mines wouldn't have been revealed

def view_board():
    game_finished_window.destroy()
    game_frame.pack()
    #for i in range(0, game.board.grid_height):
    #    for j in range(0, game.board.grid_width):
    #        tiles[i][j].config(text=game.board.grid[i][j].value, bg="white")
    #        if game.get_cell(i, j, "value") == "*":
    #            tiles[i][j].config(bg="red")
    #        if game.get_cell(i, j, "value") == "0":
    #            tiles[i][j].config(text="")
    if game.game_mode=="Time Trial" and widgets.countdown_timer.cget("text")=="00:00":
        reveal_all_mines()
    Button(game_frame, text="Menu", bg="blue", fg="white", font=15, width=10, command=lambda: return_to_menu(game_frame)).grid(row=2, column=2)
    view_mines_button = Button(game_frame, text="Hide Mines", bg="yellow", font=("Calibri", 15), width=10, command=lambda: reveal_all_mines(view_mines_button))
    view_mines_button.grid(row=3,column=2)


def start_game(game_mode, difficulty=""):
    main_menu.forget()
    global game_frame
    game_frame = Frame(Minesweeper)
    game_frame.pack()

    title = Label(game_frame, text="MINESWEEPER.PROTO", font=("Calibri", 20))
    title.grid(row=0, column=1)

    widgets.communicator = Label(game_frame, text="Click a cell to start", font=("Calibri", 18), width=24)
    widgets.communicator.grid(row=2, column=1)

    widgets.cell_grid = Frame(game_frame)
    widgets.cell_grid.grid(row=1, column=1)

    if game_mode == "Classic":
        if not difficulty:  # if this is our first time, and difficulty==""
            start_classic_mode(difficulty_button.cget("text"))
        else:
            start_classic_mode(difficulty)
    if game_mode == "Time Trial":
        start_time_trial()


def start_classic_mode(difficulty):
    game.start_classic_mode(difficulty)

    widgets.countup_timer = Label(game_frame, text="00:00", font=("Calibri", 20), width=5)
    widgets.countup_timer.grid(row=0, column=2)

    widgets.mines_left_counter = Label(game_frame, text=str(game.mines_left), font=("Calibri", 20), width=2)
    widgets.mines_left_counter.grid(row=0, column=0)

    global tiles
    tiles = [[Button(widgets.cell_grid) for _ in range(0, game.board.grid_width)] for _ in range(0, game.board.grid_height)]

    for i in range(0, game.board.grid_height):
        for j in range(0, game.board.grid_width):
            tile = Button(widgets.cell_grid, text="", width=5, height=2, bg="#d8d8d8", font=("Segoe UI", 12))
            tile.config(command=lambda row=i, column=j: ui_open_cell(row, column))
            tile.bind("<Button-2>", lambda event, row=i, column=j: ui_confuse_cell(row, column))
            tile.bind("<Button-3>", lambda event, row=i, column=j: ui_flag_cell(row, column))
            if game.difficulty == "Intermediate" or game.difficulty == "Expert":
                tile.config(width=4, height=2, font=("Segoe UI", 9))
            tile.grid(row=i + 1, column=j + 1)
            tiles[i][j] = tile


def start_time_trial():
    game.start_time_trial()

    widgets.countdown_timer = Label(game_frame, text="03:00", font=("Calibri", 20), width=5)
    widgets.countdown_timer.grid(row=0, column=2)

    widgets.mines_left_counter = Label(game_frame, text=str(game.mines_left), font=("Calibri", 20), width=2)
    widgets.mines_left_counter.grid(row=0, column=0)

    make_tt_board()


def make_tt_board():
    game.game_started = False
    widgets.cell_grid = Frame(game_frame)
    widgets.cell_grid.grid(row=1, column=1)
    global tiles
    tiles = [[Button(widgets.cell_grid) for _ in range(0, game.board.grid_width)] for _ in range(0, game.board.grid_height)]
    for i in range(0, game.board.grid_height):
        for j in range(0, game.board.grid_width):
            tile = Button(widgets.cell_grid, text="", width=5, height=2, bg="#d8d8d8", font=("Segoe UI", 12))
            tile.config(command=lambda row=i, column=j: ui_open_cell(row, column))
            tile.bind("<Button-2>", lambda event, row=i, column=j: ui_confuse_cell(row, column))
            tile.bind("<Button-3>", lambda event, row=i, column=j: ui_flag_cell(row, column))
            if game.tt_difficulty == "Hard" or game.tt_difficulty == "Very Hard":
                tile.config(width=4, height=2, font=("Segoe UI", 9))
            tile.grid(row=i + 1, column=j + 1)
            tiles[i][j] = tile


# def view_board():
#    game_finished_window.destroy()
#    game_frame.pack()
#    for i in range(0, game.board.grid_height):
#        for j in range(0, game.board.grid_width):
#            tiles[i][j].config(text=game.board.grid[i][j].value, bg="white")
#            if game.get_cell(i, j, "value") == "*":
#                tiles[i][j].config(bg="red")
#            if game.get_cell(i, j, "value") == "0":
#                tiles[i][j].config(text="")
#    Button(game_frame, text="Menu", bg="blue", fg="white", font=15, width=6, command=lambda: return_to_menu(game_frame)).grid(row=2, column=2)


Minesweeper = Tk()
Minesweeper.title("Minesweeper")

game = GameManager()
settings = Settings(Minesweeper)

# creating frames
main_menu = Frame(Minesweeper)
main_menu.pack()
game_frame = Frame(Minesweeper)
game_finished_window = Frame(Minesweeper)

# creating widgets to go into game-based frames
widgets = Widget()

tiles = []

minesweeper_flag = PhotoImage(file="Minesweeper_flag.png")

# CREATING MAIN MENU

# configuring the geometry and rows of the main menu
# main_menu.geometry("1000x1000")
main_menu.columnconfigure(0, weight=2)
main_menu.columnconfigure(1, weight=3)
main_menu.columnconfigure(2, weight=2)
main_menu.rowconfigure(0, weight=2)
main_menu.rowconfigure(1, weight=1)
main_menu.rowconfigure(2, weight=3)
main_menu.rowconfigure(3, weight=1)

# adding main widgets on the main_menu window
Label(main_menu, text="MINESWEEPER", font=("Calibri", 40), bg="white", fg="black").grid(row=0, column=1, pady=7)

classic_button = Frame(main_menu, bg="green")
for i in range(3):
    classic_button.columnconfigure(i, weight=1)
classic_button.rowconfigure(0, weight=2)
classic_button.rowconfigure(1, weight=1)
classic_label = Label(classic_button, text="Classic", font=("Calibri", 30), bg="green", width=33, height=2)
classic_label.grid(row=0, column=1)
difficulty_button = Button(classic_button, text="Beginner", font=("Calibri", 16), bg="#10401d", fg="white", width=12, command=lambda: change_difficulty(difficulty_button.cget("text")))
difficulty_button.grid(row=1, column=1)
classic_button.bind("<Button-1>", lambda event: start_game("Classic"))
classic_label.bind("<Button-1>", lambda event: start_game("Classic"))
classic_button.grid(row=1, column=1, pady=7)

# Extra options
game_modes = Frame(main_menu)
game_modes.grid(row=2, column=1)
Button(main_menu, text="Tutorial", font=("Calibri", 16), bg="green", width=11).grid(row=3, column=0)
Label(main_menu, text="PROTO", font=("Calibri", 16), bg="grey", width=15).grid(row=3, column=2)
Button(main_menu, text="Settings:gear_icon", font=("Calibri", 12), bg="grey", fg="blue", height=2, width=20, command=lambda: settings.create_settings_window(main_menu, Minesweeper)).grid(row=0,
                                                                                                                                                                                           column=0)
log_in_button = Button(main_menu, text="Log In", font=("Calibri", 15), bg="dark grey", fg="white", height=2, width=10, command=lambda: log_in())
log_in_button.grid(row=0, column=2)

# Alternative game modes/ information
Button(game_modes, text="Leaderboard", font=("Calibri", 24), bg="yellow", width=20, height=2, pady=8).grid(row=0, column=0, padx=5, pady=3)
Button(game_modes, text="Time Trial", font=("Calibri", 24), bg="blue", width=20, height=2, pady=8, command=lambda: start_game("Time Trial")).grid(row=0, column=1, padx=5, pady=3)
Button(game_modes, text="Tips", font=("Calibri", 24), bg="purple", width=20, height=2, pady=8).grid(row=1, column=0, padx=5, pady=3)
Button(game_modes, text="Statistics", font=("Calibri", 24), bg="red", width=20, height=2, pady=8).grid(row=1, column=1, padx=5, pady=3)

mainloop()