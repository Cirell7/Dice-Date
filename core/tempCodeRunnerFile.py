from math import *
x = input().split()
a, b, c = int(x[0]), int(x[1]), int(x[2])
x1,x2 = 0,0
if c > 0:
    if b > 0:
        for i in range(1, c+1):
            if c % i == 0 and -c//i - i == -b:
                x1 = -c//i
                x2 = -i
                break
    else:  # b < 0
        for i in range(1, c+1):
            if c % i == 0 and c//i + i == -b:
                x1 = c//i
                x2 = i
                break
if c < 0:
    if b > 0:
        for i in range(c,0):
            if abs(c) % i == 0 and i - abs(c)//i == -b:
                x1 = i
                x2 = -abs(c)//i
                break
    else:  # b < 0
        for i in range(c,0):
            if abs(c) % i == 0 and abs(c)//i - i == -b:
                x1 = -i
                x2 = abs(c)//i
                break
print(x1,x2)