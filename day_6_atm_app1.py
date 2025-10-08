import streamlit as st

# ---------- BankAccount class ----------
class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return f"Deposited ₹{amount}. New balance: ₹{self.__balance}"
        else:
            return "Invalid deposit amount."

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrew ₹{amount}. Remaining balance: ₹{self.__balance}"
        else:
            return "Insufficient funds."

    def get_balance(self):
        return self.__balance

# ---------- Streamlit UI ----------
st.title("OOP Bank Demo")

# ensure session_state key exists
if "account" not in st.session_state:
    st.session_state.account = None

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Account holder name", key="name_input")
    initial_balance = st.number_input("Initial balance", min_value=0, step=100, key="init_balance")

    if st.button("Create Account"):
        if not name.strip():
            st.warning("Please enter an account holder name.")
        else:
            st.session_state.account = BankAccount(name.strip(), initial_balance)
            st.success(f"Account created for {name.strip()} with balance ₹{initial_balance}")

with col2:
    # Deposit form
    with st.form("deposit_form"):
        deposit_amount = st.number_input("Deposit amount", min_value=0, step=100, key="deposit_amount")
        deposit_submit = st.form_submit_button("Deposit")
        if deposit_submit:
            if st.session_state.account is None:
                st.warning("Create an account first.")
            else:
                st.info(st.session_state.account.deposit(deposit_amount))

    # Withdraw form
    with st.form("withdraw_form"):
        withdraw_amount = st.number_input("Withdraw amount", min_value=0, step=100, key="withdraw_amount")
        withdraw_submit = st.form_submit_button("Withdraw")
        if withdraw_submit:
            if st.session_state.account is None:
                st.warning("Create an account first.")
            else:
                st.info(st.session_state.account.withdraw(withdraw_amount))

# Always show current balance if account exists
st.divider()
if st.session_state.account:
    st.write(f"**Account holder:** {st.session_state.account.account_holder}")
    st.write(f"**Current balance:** ₹{st.session_state.account.get_balance()}")
else:
    st.info("No account yet. Create one on the left.")
