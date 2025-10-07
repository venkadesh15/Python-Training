class Student:
    def read(self):
        self.name = input("Enter student name: ")
        self.age = int(input("Enter student age: "))
        self.m1 = int(input("Mark 1: "))
        self.m2 = int(input("Mark 2: "))
        self.m3 = int(input("Mark 3: "))
        self.total = self.m1 + self.m2 + self.m3

        if self.total / 3 >= 90:
            self.grade = "A+"
        elif self.total / 3 >= 80:
            self.grade = "A"
        elif self.total / 3 >= 70:
            self.grade = "B"
        elif self.total / 3 >= 60:
            self.grade = "C"
        elif self.total / 3 >= 50:
            self.grade = "D"
        else:
            self.grade = "Fail"

students = []

n = int(input("How many students? "))

for i in range(n):
    s = Student()
    s.read()
    students.append(s)

print(f"{'S.No':<5} {'Name':<25} {'Age':<5} {'Mark1':<6} {'Mark2':<6} {'Mark3':<6} {'Total':<6} {'Grade':<6}")
print("-" * 70) #an f-string-used for formatting strings,variables or expressions inside-{},<5-left-align the text
for idx, s in enumerate(students, start=1):#idx → the serial number starting from 1,enumerate(students, start=1)→loops list students
    print(f"{idx:<5} {s.name:<25} {s.age:<5} {s.m1:<6} {s.m2:<6} {s.m3:<6} {s.total:<6} {s.grade:<6}")
