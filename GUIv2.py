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


def game_state_check():
    if game.game_has_been_won:
        finish_game("Congratulations")
    elif game.board.game_over:
        finish_game("GAME OVER")


def finish_game(outcome):
    for i in range(0, game.board.grid_height):
        for j in range(0, game.board.grid_width):
            tiles[i][j].config(state=DISABLED)
    communicator.config(text=outcome)
    classic_win.after(500, lambda: create_credit_window(outcome))


def create_credit_window(outcome):
    game_finished_window = Toplevel(classic_win)
    game_finished_window.geometry("500x500")
    game_finished_window.title(outcome)
    for i in range(3):
        game_finished_window.columnconfigure(i, weight=1)
        if i == 0 or i == 3:
            game_finished_window.rowconfigure(i, weight=3)
        elif i == 1 or i == 2:
            game_finished_window.rowconfigure(i, weight=2)
    final_time = [timer.cget("text")[0:2], timer.cget("text")[3:5]]
    Label(game_finished_window, text=f"Your time was:\n {final_time[0]}:{final_time[1]}\nPlease enter your username below", font=("Calibri", 16)).grid(row=0, column=1)
    username = Entry(game_finished_window, font=("Calibri", 16))
    username.grid(row=1, column=1)
    Button(game_finished_window, text="CONFIRM", font=("Calibri", 16), command=lambda: user_info_got(game_finished_window, username.get(), final_time)).grid(row=2, column=1)


def user_info_got(window, username, time):  # where time is an array, 1st index is minutes, 2nd index is seconds
    window.destroy()
    add_user_info(username,time)


game = GameManager()

classic_win = Tk()

cell_grid = Frame(classic_win)
cell_grid.grid(row=1, column=1)

# difficulty = input("Enter difficulty:")
# game.start_classic_mode(difficulty)
game.start_classic_mode("Beginner")

tiles = [[Button(classic_win) for _ in range(0, game.board.grid_width)] for _ in range(0, game.board.grid_height)]

for i in range(0, game.board.grid_height):
    for j in range(0, game.board.grid_width):
        tile = Button(cell_grid, text="", width=5, height=2, bg="#d8d8d8", font=("Segoe UI", 12))
        current_tile = tile
        tile.config(command=lambda row=i, column=j: ui_open_cell(row, column))
        tile.bind("<Button-2>", lambda event, row=i, column=j: ui_confuse_cell(row, column))
        tile.bind("<Button-3>", lambda event, row=i, column=j: ui_flag_cell(row, column))
        if game.difficulty == "Intermediate" or game.difficulty == "Expert":
            tile.config(width=4, height=2, font=("Segoe UI", 9))
        tile.grid(row=i + 1, column=j + 1)
        tiles[i][j] = tile

title = Label(classic_win, text="MINESWEEPER.PROTO", font=("Calibri", 20))
title.grid(row=0, column=1)

communicator = Label(classic_win, text="Click a cell to start", font=("Calibri", 18), width=24)
communicator.grid(row=2, column=1)

mines_left_counter = Label(classic_win, text=str(game.mines_left), font=("Calibri", 20), width=2)
mines_left_counter.grid(row=0, column=0)

timer = Label(classic_win, text="0", font=("Calibri", 20), width=5)
timer.grid(row=0, column=2)
update_timer(0, 0)

mainloop()
