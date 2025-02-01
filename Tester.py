def triangle(height):
    for i in range(1,height+1):
        print(" "*(height-i) + "*"*(2*i - 1) + " "*(height-i))
layers = int(input("How many layers would you like the triangle to have:"))
triangle(layers)