import re

n = int(input("Enter the number of steps: "))

for s in range(1,n+1):
    spaces = " " * (n-s)
    hashtags = "#" * s
    print(spaces + hashtags)

