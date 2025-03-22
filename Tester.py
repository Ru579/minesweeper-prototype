#my_list = [0,1,2,3,4,5,6,7,8,9]
#
#length = len(my_list)
#total = 0
#for i,value in enumerate(my_list):
#    print(i, value)
#    total+=value
#    #del my_list[i]
#print(total/length)
#my_list.insert(2,99)
#print(my_list)


#with open(f"ms_user_data/Classic/Beginner/123_ClBeginner.txt") as file:
#    data = file.readlines()
#print(len(data))

#with open(f"ms_user_data/Classic/Beginner/123_ClBeginner.txt","a") as file:
with open(f"test.txt","w") as file:
    file.write("-100,999999,999999,999999,999999,999999,999999,999999,999999,999999,999999\n0,0,0\n50.8\n45.7\n43.6\n***\n")
    for i in range(100):
        file.write(str(i)+"\n")

with open("test.txt") as file:
    data = file.readlines()

def calc_100():
    start_sum = False
    total = 0
    for line in data:
        if line == "***\n":
            start_sum = True
        elif start_sum:
            #for _ in range(100):
            #    total += int(data[len(data) - 1].strip("\n"))
            #    del data[len(data) - 1]
            #for i in range(len(data)-1, 2, -1):
            #    total += int(data[i].strip("\n"))
            #    del data[i]

            i=len(data)-1
            while data[i]!="***\n":
                total+= int(data[i].strip("\n"))
                del data[i]
                i-=1
            break
    total /= 100  # calculating the average of the 100 values

    data.insert(len(data) - 1, str(total) + "\n")

    with open("test.txt","w") as file:
        for line in data:
            file.write(line)


#for i in range(len(data)-1, 2, -1):
#    del data[i]
#data.insert(len(data) - 1, f"*999\n")
#print(data)


calc_100()