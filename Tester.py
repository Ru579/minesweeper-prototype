#with open("test.txt","r") as file:
#    data = file.readlines()
#    top_10 = data[0].split(",")
#    for i in range(10):
#        top_10[i] = int(top_10[i])
#print(top_10)
#print(str(top_10)[1:len(str(top_10))-1])

#dict = {
#    "key1": "hello",
#    "key2": 23,
#    "key3": [0,1,2,3,4,5],
#    "key4":5.0
#}
#
#for i in range(6):
#    dict["key3"][i] = str(dict["key3"][i])+"2"
#
#print(dict["key3"])


def check_if_top_10_time(self, time):
    original_top_10 = self.top_10_classic
    for i in range(0, 10, -1):
        if time > self.top_10_classic[i]:
            if i != 9:
                self.top_10_classic.insert(i + 1, time)
                del self.top_10_classic[10]
            break


def check_if_top_10_stage(self, stage):
    for i in range(0, 10, -1):
        if stage < self.top_10_time_trial[i]:
            if i != 9:
                self.top_10_time_trial.insert(i + 1, stage)
                del self.top_10_time_trial[10]
            break

#test = [0,1,2,3,4,5,6,7,8,9]
#for i in range(9,-1,-1):
#    #print(i)
#    print(test[i])

#for i in range(10, -1, -1):
#    if time > self.top_10_scores[f"Cl{difficulty}"][i]:
#        if i != 10:
#            self.top_10_scores[f"Cl{difficulty}"].insert(i + 1, time)
#            del self.top_10_scores[f"Cl{difficulty}"][10]
#            self.top_10_rank = i
#            break
#        # return 100 #100 will be used to represent that the time was not in the top 10
#
#for i in range(9, -1, -1):
#    if stage<self.top_10_scores["Time Trial"][i]:
#        if i!=9:
#            self.top_10_scores["Time Trial"].insert(i+1, stage)
#            del self.top_10_scores["Time Trial"][10]
#            self.top_10_rank = i
#            break
#            #return i
#        #return 100  # 100 will be used to represent that the time was not in the top 10

string = ("[Hello]")
print(string[1:len(string)-1])