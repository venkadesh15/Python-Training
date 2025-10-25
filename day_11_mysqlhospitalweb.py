import streamlit as st
import mysql.connector as sqltor
import pandas as pd
import datetime
import random

# =========================
# Database Connection
# =========================
con = sqltor.connect(
    host="localhost",
    user="root",
    password="Venky@15",
    database="hello",
    port=3306
)
cur = con.cursor(buffered=True)

# =========================
# Setup Tables
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS appt (
    idno CHAR(12) PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender CHAR(1),
    phone CHAR(10),
    bg VARCHAR(5)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id CHAR(12) NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    room INT NOT NULL,
    appt_date DATE NOT NULL,
    appt_no INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES appt(idno) ON DELETE CASCADE
)
""")
con.commit()

# =========================
# Data
# =========================
DOCTORS = [
    ("Dr. Varun", "Cardiologist", 201),
    ("Dr. Hrithik", "Cardiologist", 202),
    ("Dr. Salman", "Psychiatrist", 203),
    ("Dr. Shahrukh", "Psychiatrist", 204),
    ("Dr. Akshay", "Otolaryngologist", 205),
    ("Dr. Amir", "Otolaryngologist", 206),
    ("Dr. Sidharth", "Rheumatologist", 207),
    ("Dr. Abhishek", "Rheumatologist", 208),
    ("Dr. Ajay", "Neurologist", 209),
    ("Dr. Ranveer", "Neurologist", 200),
    ("Dr. Irfan", "MI room", 401),
    ("Dr. John", "MI room", 402),
    ("Dr. Sanjay", "MI room", 403),
    ("Dr. Shahid", "MI room", 404),
]

SERVICES = [
    ("X-Ray", 101), ("MRI", 102), ("CT Scan", 103),
    ("Endoscopy", 104), ("Dialysis", 105), ("Ultrasound", 301),
    ("EEG", 302), ("ENMG", 303), ("ECG", 304),
]

DOCTOR_PASSWORDS = {d[0].lower(): 7001 + i for i, d in enumerate(DOCTORS)}

# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="🏥 Hospital Appointment System", layout="centered")
st.title("🏥 Simple Hospital Appointment System")
st.caption(datetime.datetime.now().strftime("Date: %A, %d %B %Y | Time: %H:%M:%S"))

menu = st.sidebar.radio("Main Menu", ["Patient", "Doctor", "Services", "Exit"])

# --------------------------
# PATIENT SECTION
# --------------------------
if menu == "Patient":
    st.header("👩‍⚕️ Patient Section")
    sub = st.radio("Select Action", ["Register", "Book Appointment", "Modify Details", "View All Patients"])

    # Register new patient
    if sub == "Register":
        with st.form("register_form"):
            idn = st.text_input("Aadhaar (12 digits)")
            name = st.text_input("Patient Name")
            age = st.number_input("Age", min_value=1, max_value=120, step=1)
            gender = st.radio("Gender", ["M", "F"], horizontal=True)
            phone = st.text_input("Phone (10 digits)")
            bg = st.selectbox("Blood Group", ["A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"])
            submit = st.form_submit_button("Register")

        if submit:
            cur.execute("SELECT * FROM appt WHERE idno=%s", (idn,))
            if cur.fetchone():
                st.warning("⚠️ Aadhaar already registered.")
            elif len(idn) == 12 and len(phone) == 10:
                cur.execute("INSERT INTO appt VALUES (%s, %s, %s, %s, %s, %s)",
                            (idn, name, age, gender, phone, bg))
                con.commit()
                st.success("✅ Registration successful!")
            else:
                st.error("Invalid Aadhaar or phone number.")

    # Book appointment
    elif sub == "Book Appointment":
        idn = st.text_input("Enter your Aadhaar to book appointment")
        if st.button("Find"):
            cur.execute("SELECT * FROM appt WHERE idno=%s", (idn,))
            row = cur.fetchone()
            if not row:
                st.error("❌ No record found. Please register first.")
            else:
                st.success(f"Patient found: {row[1]} ({row[2]} years)")
                dept = st.selectbox("Select Department", sorted(set(d[1] for d in DOCTORS)))
                if st.button("Confirm Appointment"):
                    chosen = random.choice([d for d in DOCTORS if d[1] == dept])
                    days_map = {"Cardiologist": 3, "Rheumatologist": 5, "Psychiatrist": 3,
                                "Neurologist": 6, "Otolaryngologist": 4, "MI room": 1}
                    appt_date = datetime.date.today() + datetime.timedelta(days=days_map.get(dept, 3))
                    appt_no = random.randint(10, 99)
                    cur.execute("""INSERT INTO appointments
                        (patient_id, doctor_name, department, room, appt_date, appt_no)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        (idn, chosen[0], chosen[1], chosen[2], appt_date, appt_no))
                    con.commit()
                    st.success(f"✅ Appointment booked with {chosen[0]} on {appt_date} (No: {appt_no})")

    # Modify details
    elif sub == "Modify Details":
        idn = st.text_input("Enter Aadhaar")
        if st.button("Fetch Details"):
            cur.execute("SELECT * FROM appt WHERE idno=%s", (idn,))
            row = cur.fetchone()
            if not row:
                st.error("No patient found.")
            else:
                name = st.text_input("Name", value=row[1])
                age = st.number_input("Age", value=row[2])
                gender = st.radio("Gender", ["M", "F"], index=0 if row[3] == "M" else 1)
                phone = st.text_input("Phone", value=row[4])
                bg = st.text_input("Blood Group", value=row[5])
                if st.button("Update"):
                    cur.execute("""UPDATE appt SET name=%s, age=%s, gender=%s, phone=%s, bg=%s WHERE idno=%s""",
                                (name, age, gender, phone, bg, idn))
                    con.commit()
                    st.success("✅ Updated successfully!")

    # View all patients
    elif sub == "View All Patients":
        cur.execute("SELECT * FROM appt")
        data = cur.fetchall()
        if data:
            st.dataframe(pd.DataFrame(data, columns=["Aadhaar", "Name", "Age", "Gender", "Phone", "Blood Group"]))
        else:
            st.info("No patients registered yet.")

# --------------------------
# DOCTOR SECTION
# --------------------------
elif menu == "Doctor":
    st.header("👨‍⚕️ Doctor Login")
    name = st.selectbox("Select Doctor", [d[0] for d in DOCTORS])
    pswd = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if pswd and pswd.isdigit() and int(pswd) == DOCTOR_PASSWORDS[name.lower()]:
            cur.execute("""
                SELECT a.appt_date, a.appt_no, p.name, p.age, p.idno
                FROM appointments a
                JOIN appt p ON p.idno = a.patient_id
                WHERE a.doctor_name=%s
                ORDER BY a.appt_date ASC
            """, (name,))
            rows = cur.fetchall()
            if rows:
                st.dataframe(pd.DataFrame(rows, columns=["Date", "Appt No", "Patient Name", "Age", "Aadhaar"]))
            else:
                st.info("No appointments found.")
        else:
            st.error("❌ Wrong password.")

# --------------------------
# SERVICES SECTION
# --------------------------
elif menu == "Services":
    st.header("🏥 Available Hospital Services")
    st.table(pd.DataFrame(SERVICES, columns=["Service", "Room"]))

# --------------------------
# EXIT
# --------------------------
else:
    st.write("👋 Thank you for visiting!")
