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
        st.info(f"💰 Balance: ${atm.check_balance():.2f}")
    elif action == "Deposit":
        amt = st.number_input("Amount", min_value=0.01)
        if st.button("Deposit") and atm.deposit(amt):
            st.success(f"✅ Deposited ${amt:.2f}")
    elif action == "Withdraw":
        amt = st.number_input("Amount", min_value=0.01)
        if st.button("Withdraw") and atm.withdraw(amt):
            st.success(f"✅ Withdrawn ${amt:.2f}")
    elif action == "Exit":
        atm.authenticated = False
        atm._attempts = 3
        st.success("✅ Logged out")
