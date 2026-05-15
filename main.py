from bank_account import BankAccount
from storage      import save_accounts, load_accounts


def find_account(accounts, owner):
    for acct in accounts:
        if acct.owner.lower() == owner.lower():
            return acct
    return None


def print_menu():
    print("\n── My Bank ──────────────────")
    print("1. Create account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check balance")
    print("5. Transaction history")
    print("6. List all accounts")
    print("7. Quit")
    print("─────────────────────────────")


def main():
    accounts = load_accounts()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Account owner name: ").strip()
            if find_account(accounts, name):
                print(f"Account for {name} already exists.")
            else:
                accounts.append(BankAccount(name))
                save_accounts(accounts)
                print(f"Account created for {name}.")

        elif choice == "2":
            name   = input("Account name: ").strip()
            acct   = find_account(accounts, name)
            if not acct:
                print("Account not found.")
            else:
                amount = float(input("Amount to deposit: "))
                acct.deposit(amount)
                save_accounts(accounts)

        elif choice == "3":
            name   = input("Account name: ").strip()
            acct   = find_account(accounts, name)
            if not acct:
                print("Account not found.")
            else:
                amount = float(input("Amount to withdraw: "))
                acct.withdraw(amount)
                save_accounts(accounts)

        elif choice == "4":
            name = input("Account name: ").strip()
            acct = find_account(accounts, name)
            if acct: acct.get_balance()
            else: print("Account not found.")

        elif choice == "5":
            name = input("Account name: ").strip()
            acct = find_account(accounts, name)
            if acct: acct.show_history()
            else: print("Account not found.")

        elif choice == "6":
            if not accounts:
                print("No accounts yet.")
            for acct in accounts:
                print(f"  • {acct.owner}: {acct.balance:.2f}")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1–7.")


if __name__ == "__main__":
    main()