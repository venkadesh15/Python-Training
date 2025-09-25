import random

a = random.randint(1, 20) 
print("Welcome to the game")

for i in range(1, 10):
    b = int(input("Enter Your Guess Value: "))
    if a == b:
        print("Win")
        break  
    elif a > b:
        print("Higher")
    elif a < b:
        print("Lower")
else:
    print("Game over, you didn't guess the number")
