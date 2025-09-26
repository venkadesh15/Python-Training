import random

corr_pass = input("Set the correct passcode: ")
while True:
    pas = input("Enter the passcode (or 'exit' to quit): ")
    if pas.lower() == "exit":
        quit()
    if pas == corr_pass:
        print("Passcode correct! Opening the game...\n")
        break
    print("Wrong passcode! Try again.")

while True:
    num = random.randint(1, 20)
    print("Welcome to the game ")

    for _ in range(3):
        guess = input("Enter your guess (or 'exit' to quit): ")
        if guess.lower() == "exit":
            quit()
        if not guess.isdigit():
            print("Enter numbers only!")
            continue

        guess = int(guess)
        if guess == num:
            print("You win!")
            break
        print("Higher" if num > guess else "Lower")
    else:
        print(f"Game over! The number was {num}")

    if input("Play again? (yes/exit): ").lower() == "exit":
        print("Thanks for playing! ")
        break
