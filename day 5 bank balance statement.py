class BankAccount:

    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self._account_holder = account_holder
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited ₹{amount}. New Balance: ₹{self.__balance}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew ₹{amount}. Remaining Balance: ₹{self.__balance}")
        else:
            print("Insufficient funds or invalid amount.")

    def _display_holder_info(self):
        print(f"Account Holder: {self._account_holder}")

    def __apply_bank_charges(self):
        self.__balance -= 50
        print("₹50 bank charge applied.")

    def month_end_process(self):
        self.__apply_bank_charges()
        print("Month-end processing done.")
        
ac=int(input("Enter the AC/No ="))
acn=input("Enter the AC/name =")
bal=int(input("Enter the balance amount ="))
d=int(input("Enter the deposit amount ="))
w=int(input("Enter the withdrawal amount ="))


account = BankAccount(ac, acn, bal)
account.deposit(d)
account.withdraw(w)
account._display_holder_info()
account.month_end_process()
