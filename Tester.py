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