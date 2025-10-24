import mysql.connector

# ---------------- MySQL Connection Details ----------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PORT = 3306
DB_PASSWORD = "Venky@15"
DB_NAME = "schooldb"  # Make sure this database exists in MySQL

# ---------------- Connection Function ----------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        print("❌ Couldn't connect to MySQL.")
        print("Error:", e)
        return None

# ---------------- Helper: Calculate Grade ----------------
def calculate_grade(avg_score):
    if avg_score >= 85:
        return "A"
    elif avg_score >= 75:
        return "B"
    elif avg_score >= 60:
        return "C"
    elif avg_score >= 50:
        return "D"
    else:
        return "F"

# ---------------- Create Student ----------------
def create_student():
    name = input("Enter student name: ").strip()
    age_text = input("Enter age (number): ").strip()
    avg_text = input("Enter average score (0-100): ").strip()

    if not name or not age_text.isdigit() or not avg_text.replace('.', '', 1).isdigit():
        print("Please provide a valid name, age, and average score.")
        return

    age = int(age_text)
    avg_score = float(avg_text)
    grade = calculate_grade(avg_score)

    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, average, grade) VALUES (%s, %s, %s, %s)",
        (name, age, avg_score, grade)
    )
    conn.commit()
    print(f"✅ Student added! Grade: {grade}")
    cur.close()
    conn.close()

# ---------------- Read Students ----------------
def read_students():
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, average, grade FROM students ORDER BY id")
    rows = cur.fetchall()
    if not rows:
        print("No students found. Try adding some first!")
    else:
        print("\n--- Students ---")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Avg: {row[3]} | Grade: {row[4]}")
    cur.close()
    conn.close()

# ---------------- Update Student ----------------
def update_student():
    id_text = input("Enter the ID of the student to update: ").strip()
    if not id_text.isdigit():
        print("Please enter a valid ID number.")
        return

    new_name = input("New name: ").strip()
    new_age_text = input("New age (number): ").strip()
    new_avg_text = input("New average score (0-100): ").strip()

    if not new_name or not new_age_text.isdigit() or not new_avg_text.replace('.', '', 1).isdigit():
        print("Please provide a valid name, age, and average score.")
        return

    new_age = int(new_age_text)
    new_avg = float(new_avg_text)
    new_grade = calculate_grade(new_avg)

    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name=%s, age=%s, average=%s, grade=%s WHERE id=%s",
        (new_name, new_age, new_avg, new_grade, id_text)
    )
    conn.commit()
    if cur.rowcount == 0:
        print("No student with that ID found.")
    else:
        print(f"✅ Student updated! Grade: {new_grade}")
    cur.close()
    conn.close()

# ---------------- Delete Student ----------------
def delete_student():
    id_text = input("Enter the ID of the student to delete: ").strip()
    if not id_text.isdigit():
        print("Please enter a valid ID number.")
        return

    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_text,))
    conn.commit()
    if cur.rowcount == 0:
        print("No student with that ID found.")
    else:
        print("✅ Student deleted!")
    cur.close()
    conn.close()

# ---------------- Delete All Students ----------------
def delete_all_students():
    confirm = input("Are you sure you want to delete ALL students? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Operation cancelled.")
        return

    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("DELETE FROM students")
    conn.commit()
    print("✅ All students deleted!")
    cur.close()
    conn.close()

# ---------------- Main Menu ----------------
def main():
    print("Python MySQL CRUD Demo!\n")
    while True:
        print("Choose an option:")
        print("1) Create (add a student)")
        print("2) Read (show all students)")
        print("3) Update (edit a student)")
        print("4) Delete (remove a student)")
        print("5) Delete All Students")
        print("6) Exit")
        choice = input("Your choice (1-6): ").strip()

        if choice == "1":
            create_student()
        elif choice == "2":
            read_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            delete_all_students()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3, 4, 5, or 6.\n")

if __name__ == "__main__":
    main()
