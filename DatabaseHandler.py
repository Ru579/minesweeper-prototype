import datetime

scores = {}
leaderboard = {}


def add_classic_user_info(username, time):  # where time is an array, 1st index is minutes, 2nd index is seconds
    with open("scores.txt", "r") as file:
        for line in file:
            record = line.split(":")
            scores[f"{record[0]}"] = record[1].strip("\n")
    date = datetime.datetime.now().strftime("%x").split("/")
    scores[f"{username}({date[1]}-{date[0]}-{date[2]})"] = f"{time[0]}-{time[1]}"
    with open("scores.txt", "w") as file:
        for a, b in scores.items():
            file.write(f"{a}:{b}\n")

#for the future, could keep track of what records are new, and then open the file using "a" instead of "w"
# to append the new records to the end of the file instead of writing the whole file again

def add_tt_user_info(username, time):
    with open("tt_scores.txt", "r") as file:
        for line in file:
            record = line.split(":")
            scores[f"{record[0]}"] = record[1].strip("\n")
    date = datetime.datetime.now().strftime("%x").split("/")
    scores[f"{username}({date[1]}-{date[0]}-{date[2]})"] = f"{time[0]}-{time[1]}"
    with open("tt_scores.txt", "w") as file:
        for a, b in scores.items():
            file.write(f"{a}:{b}\n")


def organise_scores():
    with open("scores.txt", "r") as file:
        for line in file:
            record = line.split(":")
            scores[f"{record[0]}"] = record[1].strip("\n")
    for name, time in scores.items():
        leaderboard[name] = str(time[0:2]) + str(time[3:5])
    sorted_list = dict(sorted(leaderboard.items(), key=lambda item: item[1]))
    print(sorted_list)  # CHECKING LINE

# TO-DO:

# if seconds>60, seconds=seconds%60, minutes+=seconds//60
# show all mines upon game over; therefore, remove view_board button
# add "retry?" Button in game_finished_window
#add powerups? eg. +minute, or cancel one mine that was clicked


# statistics option, allows you to view average time, best time, furthest level reached in time trial
# have different files for different things e.g. average time, best time ever, top 10 or 100 times (instead of organising the entire thing?), (eventually) levels for different game modes
