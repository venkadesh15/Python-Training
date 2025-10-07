class student:
    def read(self):
        self.name = input("Enter student name: ")
        self.age = int(input("Enter student age: "))
        self.m1 = int(input("Enter mark 1: "))
        self.m2 = int(input("Enter mark 2: "))
        self.m3 = int(input("Enter mark 3: "))
        self.total = self.m1 + self.m2 + self.m3
        self.avg = self.total / 3

        if self.avg >= 90:
            self.grade = "A+"
        elif self.avg >= 80:
            self.grade = "A"
        elif self.avg >= 70:
            self.grade = "B"
        elif self.avg >= 60:
            self.grade = "C"
        elif self.avg >= 50:
            self.grade = "D"
        else:
            self.grade = "Fail"

    def write(self):
        print("\n--- Student Details ---")
        print("Name:", self.name)
        print("Age:", self.age)
        print("Total:", self.total)
        print("Average:", self.avg)
        print("Grade:", self.grade)


while True:
    s1 = student()
    s1.read()
    s1.write()
