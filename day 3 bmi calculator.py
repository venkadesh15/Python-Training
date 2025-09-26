weight = float(input("Enter your weight in kg: "))
height_cm = float(input("Enter your height in cm: "))
height_m = height_cm / 100
bmi = weight / (height_m ** 2)
print(f"\nYour BMI is: {bmi:.2f}")
if bmi < 18.5:
    print("You are Underweight")
elif 18.5 <= bmi < 24.9:
    print("You are Normal weight")
elif 25 <= bmi < 29.9:
    print("You are Overweight")
else:
    print("You are Obese")