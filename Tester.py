with open("test.txt","r") as file:
    data = file.readlines()
    top_10 = data[0].split(",")
    for i in range(10):
        top_10[i] = int(top_10[i])
print(top_10)
print(str(top_10)[1:len(str(top_10))-1])