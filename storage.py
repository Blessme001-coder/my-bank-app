import json
import os
from bank_account import BankAccount

FILE = "accounts.json"

def save_accounts(accounts):
    data = [acct.to_dict() for acct in accounts]
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(accounts)} account(s) to {FILE}.")

def load_accounts():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        data = json.load(f)
    return [BankAccount.from_dict(d) for d in data]

if __name__ == "__main__":
    EzieOdoteh = BankAccount("Ezie Odoteh", 100)
    bob   = BankAccount("Bob",   250)
    EzieOdoteh.deposit(50)
    bob.withdraw(30)
    save_accounts([EzieOdoteh, bob])
    loaded = load_accounts()
    for acct in loaded:
        acct.get_balance()
        acct.show_history()