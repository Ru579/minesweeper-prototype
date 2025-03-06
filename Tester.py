import os

file = open("test.txt")

with open("test.txt", "w") as my_file:
    my_file.write("y is the best")

data = file.readlines()
print(data)