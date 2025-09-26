n = int(input("How many students? "))
students = {}

for i in range(1, n+1):
    name = input(f"\nEnter name of student {i}: ")
    sub1 = int(input("Enter mark for Subject 1: "))
    sub2 = int(input("Enter mark for Subject 2: "))
    sub3 = int(input("Enter mark for Subject 3: "))
    
    total = sub1 + sub2 + sub3
    average = total / 3
    result = "Pass" if sub1 >= 35 and sub2 >= 35 and sub3 >= 35 else "Fail"
    
    if result == "Fail":
        grade = "F"
    elif average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    else:
        grade = "C"
    
    students[name] = {"S1": sub1, "S2": sub2, "S3": sub3, "Total": total,
                      "Avg": average, "Grade": grade, "Result": result}
print(f"{'Rank':<5}{'Name':<10}{'S1':<5}{'S2':<5}{'S3':<5}{'Total':<7}{'Avg':<7}{'Grade':<7}{'Result':<7}")
print("-"*60)

rank = 1
for name, info in students.items():
    print(f"{rank:<5}{name:<10}{info['S1']:<5}{info['S2']:<5}{info['S3']:<5}"
          f"{info['Total']:<7}{info['Avg']:<7.2f}{info['Grade']:<7}{info['Result']:<7}")
    rank += 1
