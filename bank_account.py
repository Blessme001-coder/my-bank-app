# ── Phase 1: Your BankAccount class ──────────────────────────────
# Save this as bank_account.py and run it with: python bank_account.py

class BankAccount:
    """A simple bank account with deposit, withdraw, and history."""

    def __init__(self, owner, balance=0):
        self.owner   = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        """Add money to the account."""
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        self.history.append(f"Deposited {amount:.2f}")
        print(f"Deposited {amount:.2f}. New balance: {self.balance:.2f}")

    def withdraw(self, amount):
        """Remove money from the account."""
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("Insufficient funds.")
            return
        self.balance -= amount
        self.history.append(f"Withdrew {amount:.2f}")
        print(f"Withdrew {amount:.2f}. New balance: {self.balance:.2f}")

    def get_balance(self):
        """Print current balance."""
        print(f"{self.owner}'s balance: {self.balance:.2f}")

    def show_history(self):
        """Print all transactions."""
        print(f"\n── {self.owner}'s transaction history ──")
        if not self.history:
            print("  No transactions yet.")
        else:
            for entry in self.history:
                print(f"  • {entry}")

    def transfer(self, target, amount):
        """Transfer money from this account to another."""
        if amount <= 0:
            print("Amount must be positive.")
            return False
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        self.balance  -= amount
        target.balance += amount
        self.history.append(f"Transferred {amount:.2f} to {target.owner}")
        target.history.append(f"Received {amount:.2f} from {self.owner}")
        return True                  

    def to_dict(self):
        return {
            "owner":   self.owner,
            "balance": self.balance,
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data):
        acct         = cls(data["owner"], data["balance"])
        acct.history = data["history"]
        return acct            


# ── Try it out ────────────────────────────────────────────────────
if __name__ == "__main__":
    account = BankAccount("Ezie Odoteh", balance=1000000)
    account.deposit(5500)
    account.withdraw(8000)
    account.withdraw(500000)   # should print: Insufficient funds
    account.get_balance()
    account.show_history()

    def to_dict(self):
        """Convert this account to a plain dictionary for saving."""
        return {
            "owner":   self.owner,
            "balance": self.balance,
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data):
        """Recreate an account object from saved dictionary data."""
        acct         = cls(data["owner"], data["balance"])
        acct.history = data["history"]
        return acct