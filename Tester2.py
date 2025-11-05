func start_classic_mode(difficulty: str):
    difficulty = difficulty
    game_mode = "Classic"
    game_has_been_won = False
    mines_revealed = False

    if database.user_signed_in then
        increment database.glb[difficulty]["Games"]

    if difficulty = "Beginner" then
        board = Board(8, 8, 10)
        flags_left = 10
    elseif difficulty = "Intermediate" then
        board = Board(16, 16, 40)
        flags_left = 40
    elseif difficulty = "Expert" then
        board = Board(16, 30, 99)
        flags_left = 99
    else
        raise Error("Not a proper difficulty given")


func start_time_trial:
    # setting state variables
    game_mode = "Time Trial"
    board_done = False
    game_has_been_won = False
    mines_revealed = False
    swapped_to_hard_tt = False
    stage = 6
    stopwatch = 0
    tt_difficulty = "Easy"

    if database.user_signed_in then
        increment database.glb["Time Trial"]["Games"]

    board = Board(stage, stage, Call board.calculate_no_of_mines(stage, "Easy"))
    flags_left = Call board.calculate_no_of_mines(stage, "Easy")


func open_cell(x: int, y: int):
    Call board.open_cell(x, y, game_started)
    flag_difference = board.flag_difference
    board.flag_difference = 0
    if not game_started then
        game_has_been_won = False
        timer_on = True
    Call board_done_check


func board_done_check:
    if (board.revealed_cells = grid_width * grid_height - no_of_mines) and not game_over then
        if game_mode = "Classic" then
            game_has_been_won = True
        elseif game_mode = "Time Trial" then
            board_done = True
        user_can_interact = False

func update_countdown_timer(minutes: int, seconds: int):
    if timer_on then
        increment stopwatch
        decrement seconds

        if seconds < 0 then
            seconds = 59
            decrement minutes

        if (seconds = 0) and (minutes = 0) then
            game_over = True
            time_change_type = "Time Ran Out"
        else
            time_change_type = "Normal"
    else
        if time_to_be_added then
            total_time = minutes * 60 + seconds
            total_time = total_time + bonus_times[tt_difficulty]
            time_to_be_added = False

            minutes = total_time DIV 60
            seconds = total_time MOD 60
            time_change_type = "Time Added"

    return minutes, seconds


func next_tt_stage:
    timer_on = False
    increment stage

    if database.user_signed_in then
        increment database.glb["Time Trial"]["Boards"]
    Call set_difficulty

    no_of_mines = Call board.calculate_no_of_mines(stage, tt_difficulty)
    board = Board(stage, stage, no_of_mines)
    flags_left = no_of_mines

    board_done = False
    if tt_difficulty = "Hard" and not swapped_to_hard_tt then
        swapped_to_hard_tt = True


func set_difficulty:
    if stage < 10 then
        tt_difficulty = "Easy"
    elseif 10 <= stage <= 16 then
        tt_difficulty = "Medium"
    elseif 17 <= stage <= 23 then
        tt_difficulty = "Hard"
    elseif 24 <= stage then
        tt_difficulty = "Very Hard"
# easy to expand this function to add more difficulties depending on how well players perform- this will be discovered during testing

func finish_game(final_score: int, outcome: str, mine_clicked: Bool):
    if database.user_signed_in then
        # adding the score to the database and updating the ranking of the top 10 scores
        if game_mode = "Time Trial" then
            Call database.add_tt_stage(score = stage - 5, mine_clicked, stopwatch_value)
            Call reset_top_10_info
        elseif game_mode = "Classic" then
            if outcome = "WIN" then
                Call database.add_classic_time(final_score, current_difficulty)
                Call reset_top_10_info
            elseif outcome = "LOSE" then
                Call database.add_classic_loss(final_score, current_difficulty)

func reset_top_10_info:
    top_10_rank = database.top_10_rank
    no_1_status = database.no_1_status
    database.top_10_rank = Null
    database.no_1_status = Null

func determine_GUI_output_statement(current_communicator_text: str):
    if top_10_rank != Null then
        if not (game_mode == "Time Trial" and stage = 6) then
            if no_1_status = "Reached" then
                output_statement = "NEW HIGHSCORE"
            elseif no_1_status = "Tied" then
                output_statement = "So Close- you have tied with your best score"
            else
                output_statement = "Top 10 Score Achieved" + top_10_rank
            return current_communicator_text + "\n" + output_statement
    return current_communicator_text

UTILITY FUNCTION
func get_cell(x: int, y: int, info_needed: str):
    if info_needed = "value" then
        return board.grid[x][y].value
    elseif info_needed = "state" then
        return board.grid[x][y].state

