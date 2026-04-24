def update_top_10(score, top_10_scores, game_mode):
    no_1_status = "not achieved"
    for i in range(9, -1, -1):
        if (
            (score >= top_10_scores[i] and game_mode=="Classic") or 
            (score <= top_10_scores[i] and game_mode=="Time Trial")
        ): # if achieved a worse or equal score
            top_10_scores.insert(i+1, score)
            del top_10_scores[10]
            top_10_rank = i+2 # +2 because we insert after the current index AND ranks start at 1, not 0
            break
        elif i==0:
            top_10_scores.insert(0, score)
            top_10_rank = 1
            no_1_status = "Reached"
        
        # determining if player has tied with top score
        if score == top_10_scores[0]:
            no_1_status = "Tied"
    
    print(top_10_rank, no_1_status)
    return top_10_scores

#with open("ms_user_data/Classic/Beginner/test_ClBeginner.txt", "a") as file:
#    for i in range(1, 100):
#        file.write(f"{i}\n")
#file.close()

car = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

print(True if "Ford" in car else False)


#classic_top_10 = [20,22,24,26,32,46,52,68,77,82][::-1]
#classic_top_10 = update_top_10(23, classic_top_10, "Time Trial")
##classic_top_10 = update_top_10(56, classic_top_10, "Time Trial")
#print(classic_top_10)

#bottom_entry_index = len(self.user_file_data[specific_game_mode]) - 1
#
#    for line in game_file:
#        if line == "***\n":
#            start_sum = True # beginning the sum once we reach the line marking the start of the exact scores
#        elif start_sum:
#            bottom_entry_index = len(game_file) - 1
#            
#            # 
#            while game_file[bottom_entry_index] != "***\n":
#                total_score += int(game_file[bottom_entry_index].strip("\n"))
#                del self.user_file_data[specific_game_mode][bottom_entry_index] # accessing the attribute directly for deletion
#                bottom_entry_index -= 1
#            break

#test = "False"
#print(bool(test))
#if not test:
#    print("no string here")
#if not bool(test):
#    print("string is false")
#if bool(test):
#    print("The string says True")