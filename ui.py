import tkinter as tk
from tkinter import messagebox
from bank_account import BankAccount
from storage import save_accounts, load_accounts

BG        = "#1A1A2E"
BG2       = "#16213E"
BG3       = "#0F3460"
ACCENT    = "#1D9E75"
ACCENT2   = "#7F77DD"
WARN      = "#E07B39"
BLUE      = "#2E86AB"
TEXT      = "#E0E0FF"
TEXT2     = "#8888AA"
LOG_BG    = "#12122A"


class BankApp:

    def __init__(self, root):
        self.root = root
        self.root.title("THE BANK OF ODOTEH")
        self.root.geometry("460x620")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.accounts = load_accounts()
        self.build_ui()

    def build_ui(self):
        hdr = tk.Frame(self.root, bg=BG2, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏦  THE BANK OF ODOTEH", bg=BG2,
                 fg=TEXT, font=("Helvetica", 22, "bold")).pack()
        tk.Label(hdr, text="Secure • Simple • Yours", bg=BG2,
                 fg=TEXT2, font=("Helvetica", 10)).pack()

        inp = tk.Frame(self.root, bg=BG, pady=14, padx=20)
        inp.pack(fill="x")
        tk.Label(inp, text="ACCOUNT NAME", bg=BG,
                 fg=TEXT2, font=("Helvetica", 9, "bold"),
                 anchor="w").pack(fill="x")
        self.name_entry = tk.Entry(inp, font=("Helvetica", 13),
                                    bg=BG3, fg=TEXT, insertbackground=TEXT,
                                    relief="flat", bd=8)
        self.name_entry.pack(fill="x", pady=(2,10))
        tk.Label(inp, text="AMOUNT", bg=BG,
                 fg=TEXT2, font=("Helvetica", 9, "bold"),
                 anchor="w").pack(fill="x")
        self.amount_entry = tk.Entry(inp, font=("Helvetica", 13),
                                      bg=BG3, fg=TEXT, insertbackground=TEXT,
                                      relief="flat", bd=8)
        self.amount_entry.pack(fill="x", pady=(2,0))
        tk.Label(inp, text="TO ACCOUNT (transfer only)", bg=BG,
                 fg=TEXT2, font=("Helvetica", 9, "bold"),
                 anchor="w").pack(fill="x")
        self.to_entry = tk.Entry(inp, font=("Helvetica", 13),
                                   bg=BG3, fg=TEXT, insertbackground=TEXT,
                                   relief="flat", bd=8)
        self.to_entry.pack(fill="x", pady=(2,0))

        btn_frame = tk.Frame(self.root, bg=BG, padx=20, pady=14)
        btn_frame.pack(fill="x")
        buttons = [
            ("＋  Create Account", self.create_account, BLUE),
            ("↑   Deposit",         self.deposit,        ACCENT),
            ("↓   Withdraw",        self.withdraw,       WARN),
            ("💰  Balance",         self.check_balance,  ACCENT2),
            ("⇄   Transfer",        self.transfer,       "#2A9D8F"),
            ("🗑   Delete Account", self.delete_account,  "#C0392B"),
        ]
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        for i, (label, cmd, color) in enumerate(buttons):
            tk.Button(btn_frame, text=label, command=cmd,
                      bg=color, fg="white",
                      font=("Helvetica", 11, "bold"),
                      relief="flat", bd=0, pady=10,
                      cursor="hand2", activebackground=color,
                      activeforeground="white"
                      ).grid(row=i//2, column=i%2,
                             padx=4, pady=4, sticky="ew")

        log_frame = tk.Frame(self.root, bg=BG, padx=20)
        log_frame.pack(fill="both", expand=True)
        tk.Label(log_frame, text="TRANSACTION LOG", bg=BG,
                 fg=TEXT2, font=("Helvetica", 9, "bold"),
                 anchor="w").pack(fill="x", pady=(0,4))
        self.log = tk.Text(log_frame, height=8, bg=LOG_BG, fg=TEXT,
                           font=("Courier", 10), relief="flat",
                           state="disabled", padx=8, pady=6)
        self.log.pack(fill="both", expand=True)
        self.log.tag_config("green",  foreground=ACCENT)
        self.log.tag_config("orange", foreground=WARN)
        self.log.tag_config("purple", foreground=ACCENT2)
        self.log.tag_config("dim",    foreground=TEXT2)

        acct_frame = tk.Frame(self.root, bg=BG, padx=20, pady=10)
        acct_frame.pack(fill="x")
        tk.Label(acct_frame, text="ALL ACCOUNTS", bg=BG,
                 fg=TEXT2, font=("Helvetica", 9, "bold"),
                 anchor="w").pack(fill="x", pady=(0,4))
        self.accounts_box = tk.Text(acct_frame, height=4, bg=LOG_BG,
                                    fg=TEXT, font=("Courier", 10),
                                    relief="flat", state="disabled",
                                    padx=8, pady=6)
        self.accounts_box.pack(fill="x", pady=(0,10))
        self.refresh_accounts_box()

    def log_message(self, msg, tag="green"):
        self.log.config(state="normal")
        self.log.insert(tk.END, msg + "\n", tag)
        self.log.see(tk.END)
        self.log.config(state="disabled")

    def refresh_accounts_box(self):
        self.accounts_box.config(state="normal")
        self.accounts_box.delete("1.0", tk.END)
        if not self.accounts:
            self.accounts_box.insert(tk.END, "  No accounts yet.\n")
        for a in self.accounts:
            self.accounts_box.insert(tk.END,
                f"  • {a.owner:<22} {a.balance:>10.2f}\n")
        self.accounts_box.config(state="disabled")

    def get_account(self, name):
        for a in self.accounts:
            if a.owner.lower() == name.lower():
                return a
        return None

    def get_inputs(self):
        return self.name_entry.get().strip(), \
               self.amount_entry.get().strip()

    def create_account(self):
        name, _ = self.get_inputs()
        if not name:
            messagebox.showwarning("Missing", "Please enter a name.")
            return
        if self.get_account(name):
            messagebox.showwarning("Exists", f"{name} already exists.")
            return
        self.accounts.append(BankAccount(name))
        save_accounts(self.accounts)
        self.log_message(f"✔  Account created: {name}", "green")
        self.refresh_accounts_box()

    def deposit(self):
        name, amount = self.get_inputs()
        acct = self.get_account(name)
        if not acct:
            messagebox.showerror("Not found", f"No account for {name}.")
            return
        try:
            acct.deposit(float(amount))
            save_accounts(self.accounts)
            self.log_message(
                f"↑  Deposited {float(amount):.2f} → {name} (Balance: {acct.balance:.2f})",
                "green")
            self.refresh_accounts_box()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def withdraw(self):
        name, amount = self.get_inputs()
        acct = self.get_account(name)
        if not acct:
            messagebox.showerror("Not found", f"No account for {name}.")
            return
        try:
            acct.withdraw(float(amount))
            save_accounts(self.accounts)
            self.log_message(
                f"↓  Withdrew {float(amount):.2f} → {name} (Balance: {acct.balance:.2f})",
                "orange")
            self.refresh_accounts_box()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def check_balance(self):
        name, _ = self.get_inputs()
        acct = self.get_account(name)
        if not acct:
            messagebox.showerror("Not found", f"No account for {name}.")
            return
        self.log_message(
            f"💰 {name}'s balance: {acct.balance:.2f}", "purple")

    def transfer(self):
        name, amount = self.get_inputs()
        to_name = self.to_entry.get().strip()
        from_acct = self.get_account(name)
        to_acct   = self.get_account(to_name)
        if not from_acct:
            messagebox.showerror("Not found", f"No account: {name}")
            return
        if not to_acct:
            messagebox.showerror("Not found", f"No account: {to_name}")
            return
        if from_acct == to_acct:
            messagebox.showwarning("Same account", "Cannot transfer to same account.")
            return
        try:
            success = from_acct.transfer(to_acct, float(amount))
            if success:
                save_accounts(self.accounts)
                self.log_message(
                    f"⇄  Transferred {float(amount):.2f}: {name} → {to_name}",
                    "green")
                self.refresh_accounts_box()
            else:
                messagebox.showerror("Failed", "Insufficient funds.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")

    def delete_account(self):
        name, _ = self.get_inputs()
        acct = self.get_account(name)
        if not acct:
            messagebox.showerror("Not found", f"No account: {name}")
            return
        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {name}'s account?\nBalance: {acct.balance:.2f}\n\nThis cannot be undone."
        )
        if confirmed:
            self.accounts.remove(acct)
            save_accounts(self.accounts)
            self.log_message(f"🗑  Account deleted: {name}", "orange")
            self.refresh_accounts_box()        


if __name__ == "__main__":
    root = tk.Tk()
    app  = BankApp(root)
    root.mainloop()