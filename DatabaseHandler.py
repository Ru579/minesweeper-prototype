import datetime

scores = {}


def add_user_info(username, time):  # where time is an array, 1st index is minutes, 2nd index is seconds
    with open("scores.txt", "r") as file:
        for line in file:
            record = line.split(":")
            scores[f"{record[0]}"] = record[1].strip("\n")
    date = datetime.datetime.now().strftime("%x").split("/")
    scores[f"{username}({date[1]}-{date[0]}-{date[2]})"] = f"{time[0]}-{time[1]}"
    with open("scores.txt", "w") as file:
        for a, b in scores.items():
            file.write(f"{a}:{b}\n")

#TO-DO:
#only add winners' scores to the database
#organise database? shortest time at the top?
#add menu, with option to view leaderboard
#have different files for different things e.g. average time, best time ever, top 10 or 100 times (instead of organising the entire thing?), (eventually) levels for different game modes