import mysql.connector

# ---------------- MySQL Connection ----------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PORT = 3306
DB_PASSWORD = "Venky@15"
DB_NAME = "bankdb"

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
        print("❌ Connection Error:", e)
        return None

# ---------------- Create Account ----------------
def create_account():
    name = input("Enter name: ").strip()
    account_no = input("Set Account Number: ").strip()
    pin = input("Set 4-digit PIN: ").strip()
    age = input("Enter age: ").strip()
    amount = input("Enter initial deposit: ").strip()

    if not name or not account_no.isdigit() or not pin.isdigit() or len(pin) != 4 or not age.isdigit() or not amount.replace('.', '', 1).isdigit():
        print("⚠️ Invalid input.")
        return

    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    
    # Check if account number already exists
    cur.execute("SELECT * FROM accounts WHERE account_no=%s", (account_no,))
    if cur.fetchone():
        print("⚠️ This Account Number already exists. Please choose a different one.")
        cur.close()
        conn.close()
        return

    cur.execute("INSERT INTO accounts (account_no, name, pin, age, balance) VALUES (%s, %s, %s, %s, %s)", 
                (account_no, name, pin, int(age), float(amount)))
    conn.commit()
    print(f"✅ Account created successfully for {name}! Your Account Number: {account_no}")
    cur.close()
    conn.close()

# ---------------- Read Accounts ----------------
def read_accounts():
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("SELECT account_no, name, age, balance FROM accounts ORDER BY account_no")
    rows = cur.fetchall()
    if not rows:
        print("⚠️ No accounts found.")
    else:
        print("\n--- Account List ---")
        for r in rows:
            print(f"Account No: {r[0]} | Name: {r[1]} | Age: {r[2]} | Balance: ₹{r[3]}")
    cur.close()
    conn.close()

# ---------------- Update Account ----------------
def update_account():
    account_no = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    if not account_no.isdigit() or not pin.isdigit():
        print("⚠️ Invalid input.")
        return

    new_name = input("Enter new name: ").strip()
    new_age = input("Enter new age: ").strip()

    if not new_name or not new_age.isdigit():
        print("⚠️ Invalid name or age.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE accounts SET name=%s, age=%s WHERE account_no=%s AND pin=%s",
                (new_name, int(new_age), account_no, pin))
    conn.commit()
    if cur.rowcount == 0:
        print("❌ No matching account or wrong PIN.")
    else:
        print("✅ Account updated successfully!")
    cur.close()
    conn.close()

# ---------------- Delete Account ----------------
def delete_account():
    account_no = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    if not account_no.isdigit() or not pin.isdigit():
        print("⚠️ Invalid input.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM accounts WHERE account_no=%s AND pin=%s", (account_no, pin))
    conn.commit()
    if cur.rowcount == 0:
        print("❌ Invalid Account Number or PIN.")
    else:
        print("✅ Account deleted successfully!")
    cur.close()
    conn.close()

# ---------------- Withdraw Money ----------------
def withdraw_money():
    account_no = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()
    amount_text = input("Enter amount to withdraw: ").strip()

    if not account_no.isdigit() or not pin.isdigit() or not amount_text.replace('.', '', 1).isdigit():
        print("⚠️ Invalid input.")
        return

    amount = float(amount_text)
    if amount <= 0:
        print("⚠️ Enter positive amount.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE account_no=%s AND pin=%s", (account_no, pin))
    row = cur.fetchone()
    if not row:
        print("❌ Invalid account or PIN.")
    elif row[0] < amount:
        print("⚠️ Insufficient balance.")
    else:
        cur.execute("UPDATE accounts SET balance = balance - %s WHERE account_no=%s AND pin=%s", 
                    (amount, account_no, pin))
        conn.commit()
        print(f"✅ ₹{amount} withdrawn successfully!")
    cur.close()
    conn.close()

# ---------------- Check Balance ----------------
def check_balance():
    account_no = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, balance FROM accounts WHERE account_no=%s AND pin=%s", (account_no, pin))
    row = cur.fetchone()
    if row:
        print(f"👤 Name: {row[0]} | 💰 Balance: ₹{row[1]}")
    else:
        print("❌ Invalid Account Number or PIN.")
    cur.close()
    conn.close()

# ---------------- Main Menu ----------------
def main():
    print("\n🏦 Python + MySQL Bank System 🏦")
    while True:
        print("\n1️⃣ Create Account")
        print("2️⃣ View All Accounts")
        print("3️⃣ Update Account")
        print("4️⃣ Delete Account")
        print("5️⃣ Withdraw Money")
        print("6️⃣ Check Balance")
        print("7️⃣ Exit")
        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            read_accounts()
        elif choice == "3":
            update_account()
        elif choice == "4":
            delete_account()
        elif choice == "5":
            withdraw_money()
        elif choice == "6":
            check_balance()
        elif choice == "7":
            print("👋 Thank you for using our Bank System!")
            break
        else:
            print("⚠️ Invalid choice, try again.")

if __name__ == "__main__":
    main()