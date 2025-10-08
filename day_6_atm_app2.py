import streamlit as st

class BankAccount:
    def __init__(self, holder, balance=1000, pin="1234"):
        self.holder = holder
        self._pin = pin
        self.__balance = balance

    def check_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

    def _verify_pin(self, pin_input):
        return pin_input == self._pin

class ATM(BankAccount):
    def __init__(self, holder):
        super().__init__(holder)
        self._attempts = 3
        self.authenticated = False

    def login(self, pin_input):
        self.authenticated = self._verify_pin(pin_input)
        if not self.authenticated:
            self._attempts -= 1
        return self.authenticated

    def atm_check_balance(self):
        return f"💰 Balance: ${self.check_balance():.2f}"

    def atm_deposit(self, amount):
        if self.deposit(amount):
            return f"✅ Deposited ${amount:.2f}. New balance: ${self.check_balance():.2f}"
        return "❌ Invalid deposit amount."

    def atm_withdraw(self, amount):
        if self.withdraw(amount):
            return f"✅ Withdrawn ${amount:.2f}. New balance: ${self.check_balance():.2f}"
        return "❌ Insufficient funds."

    def atm_exit(self):
        self.authenticated = False
        self._attempts = 3
        return "✅ Logged out"

if 'atm' not in st.session_state:
    st.session_state.atm = ATM("Venkadesh")

atm = st.session_state.atm
st.title("💳 ATM")

pin = st.text_input("PIN", type="password")
action = st.radio("Select", ["Check Balance", "Deposit", "Withdraw", "Exit"])

if pin and not atm.authenticated:
    if atm.login(pin):
        st.success("✅ Logged in")
    elif atm._attempts <= 0:
        st.error("🚫 Too many attempts")
    else:
        st.error(f"❌ Wrong PIN ({atm._attempts} left)")

if atm.authenticated:
    if action == "Check Balance":
        st.info(atm.atm_check_balance())
    elif action == "Deposit":
        amt = st.number_input("Amount", min_value=0.01)
        if st.button("Deposit"):
            st.success(atm.atm_deposit(amt))
    elif action == "Withdraw":
        amt = st.number_input("Amount", min_value=0.01)
        if st.button("Withdraw"):
            st.success(atm.atm_withdraw(amt))
    elif action == "Exit":
        st.success(atm.atm_exit())

