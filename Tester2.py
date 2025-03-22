#start_end = []
#for i,line in enumerate(self.user_file_data[specific_game_mode]):
#    if line=="***":
#        start_sum = True
#        start_end.append(i)
#    elif start_sum:
#        total+=int(line)
#average = total/100

with open(f"ms_user_data/Classic/Beginner/123_ClBeginner.txt","a") as file:
    for i in range(100):
        file.write(str(i)+"\n")