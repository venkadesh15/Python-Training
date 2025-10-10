import json
import os

# JSON file to store account data
DATA_FILE = "day_8_load_data1.json"
data = {}

# -------------------- Load & Save --------------------

def load_data():
    """Load account data from JSON file."""
    global data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("⚠️ Error loading data. Creating new file...")
            data = {}
            save_data()
    else:
        data = {}
        save_data()

def save_data():
    """Save account data to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# -------------------- View Accounts --------------------

def view_accounts():
    """Display all accounts."""
    if not data:
        print("No accounts found.")
        return
    print("\n--- All Bank Accounts ---")
    for acc_no, details in data.items():
        print(f"Account No: {acc_no}")
        print(f"Name      : {details['name']}")
        print(f"Balance   : ₹{details['balance']}")
        print("-" * 30)

# -------------------- Add Account --------------------

def add_account():
    """Add a new account."""
    acc_no = input("Enter account number: ")
    if acc_no in data:
        print("⚠️ Account already exists!")
        return
    name = input("Enter account holder name: ")
    try:
        balance = float(input("Enter initial balance: "))
    except ValueError:
        print("❌ Invalid balance amount.")
        return

    data[acc_no] = {"name": name, "balance": balance}
    save_data()
    print("✅ Account added successfully!")

# -------------------- Update Account --------------------

def update_account():
    """Update existing account details."""
    acc_no = input("Enter account number to update: ")
    if acc_no not in data:
        print("❌ Account not found!")
        return

    print(f"Current Name    : {data[acc_no]['name']}")
    print(f"Current Balance : ₹{data[acc_no]['balance']}")
    
    name = input("Enter new name (leave blank to keep same): ")
    balance_input = input("Enter new balance (leave blank to keep same): ")

    if name.strip():
        data[acc_no]['name'] = name
    if balance_input.strip():
        try:
            data[acc_no]['balance'] = float(balance_input)
        except ValueError:
            print("⚠️ Invalid balance input. Keeping old balance.")
    
    save_data()
    print("✅ Account updated successfully!")

# -------------------- Delete Account --------------------

def delete_account():
    """Delete an existing account."""
    acc_no = input("Enter account number to delete: ")
    if acc_no not in data:
        print("❌ Account not found!")
        return
    
    confirm = input(f"Are you sure you want to delete account {acc_no}? (y/n): ")
    if confirm.lower() == 'y':
        del data[acc_no]
        save_data()
        print("🗑️ Account deleted successfully!")
    else:
        print("❌ Deletion cancelled.")

# -------------------- Main Menu --------------------

def main():
    """Main program loop."""
    load_data()
    while True:
        print("\n--- Bank Management ---")
        print("1. View Accounts")
        print("2. Add Account")
        print("3. Update Account")
        print("4. Delete Account")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_accounts()
        elif choice == "2":
            add_account()
        elif choice == "3":
            update_account()
        elif choice == "4":
            delete_account()
        elif choice == "5":
            print("👋 Exiting... Have a nice day!")
            break
        else:
            print("❌ Invalid choice! Try again.")

# -------------------- Entry Point --------------------

if __name__ == "__main__":
    main()
