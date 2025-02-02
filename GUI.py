from GameManager import *
from tkinter import *


def ui_open_cell(x, y):
    game.open_cell(x, y)
    update_ui()
    communicator.config(text="")
    if game.flag_difference < 0:
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if game.board.in_bounds(i, j) and game.get_cell(i, j, "state") == "Hidden":
                    tiles[i][j].config(bg="purple")
                    tiles[i][j].after(500, lambda row=i, column=j: tiles[row][column].config(bg="#d8d8d8"))
        communicator.config(text=f"Cell has {-1 * game.flag_difference} too few flags.")
    if game.flag_difference > 0:
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if game.board.in_bounds(i, j) and game.get_cell(i, j, "state") == "Flagged":
                    tiles[i][j].config(bg="purple")
                    tiles[i][j].after(500, lambda row=i, column=j: tiles[row][column].config(bg="blue"))
        communicator.config(text=f"Cell has {game.flag_difference} too many flags.")

    game_state_check()


def ui_flag_cell(x, y):
    game.flag_cell(x, y)
    if game.get_cell(x, y, "state") == "Flagged":
        tiles[x][y].config(bg="blue", text="")
    elif game.get_cell(x, y, "state") == "Hidden":
        tiles[x][y].config(bg="#d8d8d8", text="")
        if game.board.not_enough_flags:
            communicator.config(text="Not enough flags")
            communicator.after(500, lambda: communicator.config(text=""))
            game.board.not_enough_flags = False
    mines_left_counter.config(text=str(game.mines_left))


def ui_confuse_cell(x, y):
    game.confuse_cell(x, y)
    if game.get_cell(x, y, "state") == "Confused":
        tiles[x][y].config(bg="green", text="?")
    if game.get_cell(x, y, "state") == "Hidden":
        tiles[x][y].config(bg="#d8d8d8", text="")
    mines_left_counter.config(text=str(game.mines_left))


def update_ui():
    for i in range(0, game.board.grid_height):
        for j in range(0, game.board.grid_width):
            if game.get_cell(i, j, "state") == "Revealed":
                tiles[i][j].config(text=game.board.grid[i][j].value, bg="white")
                if game.get_cell(i, j, "value") == "*":
                    tiles[i][j].config(bg="red")
                if game.get_cell(i, j, "value") == "0":
                    tiles[i][j].config(text="")


def update_timer(minutes, seconds):
    seconds += 1
    if seconds == 60:
        seconds = 0
        minutes += 1
    timer.config(text=f"{minutes:02}:{seconds:02}")
    timer.after(1000, lambda: update_timer(minutes, seconds))


def change_difficulty(difficulty):
    if difficulty == "Beginner":
        difficulty_button.config(text="Intermediate")
    elif difficulty == "Intermediate":
        difficulty_button.config(text="Expert")
    elif difficulty == "Expert":
        difficulty_button.config(text="Beginner")


def game_state_check():
    if game.game_has_been_won:
        finish_game("WIN", "Congratulations!")
        game.game_started=False
    elif game.board.game_over:
        finish_game("LOSE", "GAME OVER")
        game.game_started=False


def finish_game(outcome, message):
    for i in range(0, game.board.grid_height):
        for j in range(0, game.board.grid_width):
            tiles[i][j].config(state=DISABLED)
    communicator.config(text=message)
    game_frame.after(500, lambda: create_game_finished_window(outcome))


def create_game_finished_window(outcome):
    final_time = [timer.cget("text")[0:2], timer.cget("text")[3:5]]
    timer.destroy()
    Label(game_frame, text=f"{final_time[0]}:{final_time[1]}", font=("Calibri", 20), width=5).grid(row=0, column=2)
    game_frame.forget()
    global game_finished_window
    game_finished_window = Frame(Minesweeper)
    game_finished_window.pack()
    for i in range(3):
        game_finished_window.columnconfigure(i, weight=1)
        if i == 0 or i == 3:
            game_finished_window.rowconfigure(i, weight=3)
        elif i == 1 or i == 2:
            game_finished_window.rowconfigure(i, weight=2)
    if outcome == "WIN":
        Label(game_finished_window, text=f"Your time was:\n {final_time[0]}:{final_time[1]}\nPlease enter your username below", font=("Calibri", 16)).grid(row=0, column=1)
        username = Entry(game_finished_window, font=("Calibri", 16))
        username.grid(row=1, column=1)
        Button(game_finished_window, text="CONFIRM", font=("Calibri", 16), command=lambda: user_info_get(username.get(), final_time)).grid(row=2, column=1)
    elif outcome == "LOSE":
        Label(game_finished_window, text=f"GAME OVER!\nYour time was {final_time[0]}:{final_time[1]}", font=("Calibri", 16)).grid(row=0, column=1)
        Button(game_finished_window, text="View Board?", font=("Calibri", 16), command=lambda: view_board()).grid(row=2, column=1)
        Button(game_finished_window, text="Close", font=("Calibri", 16), command=lambda: return_to_menu(game_finished_window)).grid(row=3, column=1)


def user_info_get(username, time):  # where time is an array, 1st index is minutes, 2nd index is seconds
    add_user_info(username, time)
    return_to_menu(game_finished_window)


def return_to_menu(frame):
    frame.after(500, lambda: frame.destroy())
    main_menu.after(500, lambda: main_menu.pack())


def view_board():
    game_finished_window.destroy()
    game_frame.pack()
    for i in range(0, game.board.grid_height):
        for j in range(0, game.board.grid_width):
            tiles[i][j].config(text=game.board.grid[i][j].value, bg="white")
            if game.get_cell(i, j, "value") == "*":
                tiles[i][j].config(bg="red")
            if game.get_cell(i, j, "value") == "0":
                tiles[i][j].config(text="")
    Button(game_frame, text="Menu", bg="blue", fg="white", font=15, width=6, command=lambda: return_to_menu(game_frame)).grid(row=2, column=2)


def start_game(game_mode):
    main_menu.forget()
    global game_frame
    game_frame = Frame(Minesweeper)
    game_frame.pack()

    title = Label(game_frame, text="MINESWEEPER.PROTO", font=("Calibri", 20))
    title.grid(row=0, column=1)

    global communicator
    communicator = Label(game_frame, text="Click a cell to start", font=("Calibri", 18), width=24)
    communicator.grid(row=2, column=1)

    global timer
    timer = Label(game_frame, text="00:00", font=("Calibri", 20), width=5)
    timer.grid(row=0, column=2)
    timer.after(1000, lambda: update_timer(0, 0))

    global cell_grid
    cell_grid=Frame(game_frame)
    cell_grid.grid(row=1, column=1)

    if game_mode == "Classic":
        start_classic_mode(difficulty_button.cget("text"))


def start_classic_mode(difficulty):
    game.start_classic_mode(difficulty)

    global mines_left_counter
    mines_left_counter = Label(game_frame, text=str(game.mines_left), font=("Calibri", 20), width=2)
    mines_left_counter.grid(row=0, column=0)

    global tiles
    tiles = [[Button(cell_grid) for _ in range(0, game.board.grid_width)] for _ in range(0, game.board.grid_height)]

    for i in range(0, game.board.grid_height):
        for j in range(0, game.board.grid_width):
            tile = Button(cell_grid, text="", width=5, height=2, bg="#d8d8d8", font=("Segoe UI", 12))
            tile.config(command=lambda row=i, column=j: ui_open_cell(row, column))
            tile.bind("<Button-2>", lambda event, row=i, column=j: ui_confuse_cell(row, column))
            tile.bind("<Button-3>", lambda event, row=i, column=j: ui_flag_cell(row, column))
            if game.difficulty == "Intermediate" or game.difficulty == "Expert":
                tile.config(width=4, height=2, font=("Segoe UI", 9))
            tile.grid(row=i + 1, column=j + 1)
            tiles[i][j] = tile


Minesweeper = Tk()
Minesweeper.title("Minesweeper")

game = GameManager()

# creating frames
main_menu = Frame(Minesweeper)
main_menu.pack()
game_frame = Frame(Minesweeper)
# time_trial_win = Frame(Minesweeper)
game_finished_window = Frame(Minesweeper)

# creating widgets to go into game-based frames
cell_grid = Frame(game_frame)
mines_left_counter = Label(Minesweeper)
timer = Label(Minesweeper)
communicator = Label(Minesweeper)

tiles = []

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

# Button(main_menu, text="CLASSIC", font=("Calibri", 30), bg="green", width=33, height=2, command=lambda: start_game("Classic")).grid(row=1, column=1, pady=7)

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

game_modes = Frame(main_menu)
game_modes.grid(row=2, column=1)
Button(main_menu, text="Tutorial", font=("Calibri", 16), bg="green", width=11).grid(row=3, column=0)
Label(main_menu, text="PROTO", font=("Calibri", 16), bg="grey", width=15).grid(row=3, column=2)

# Button(game_modes, text="CLASSIC", font=("Calibri", 24), bg="green", width=30).grid(row=0,column=1)
Button(game_modes, text="Leaderboard", font=("Calibri", 24), bg="yellow", width=20, height=2, pady=8).grid(row=0, column=0, padx=5, pady=3)
Button(game_modes, text="Time Trial", font=("Calibri", 24), bg="blue", width=20, height=2, pady=8).grid(row=0, column=1, padx=5, pady=3)
Button(game_modes, text="Tips", font=("Calibri", 24), bg="purple", width=20, height=2, pady=8).grid(row=1, column=0, padx=5, pady=3)
Button(game_modes, text="Statistics", font=("Calibri", 24), bg="red", width=20, height=2, pady=8).grid(row=1, column=1, padx=5, pady=3)

mainloop()
