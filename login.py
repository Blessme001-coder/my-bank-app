import tkinter as tk
from tkinter import messagebox
from users import login, register

BG      = "#1A1A2E"
PANEL   = "#252540"
TEXT    = "#E0E0FF"
SUBTEXT = "#9090B0"
ACCENT  = "#1D9E75"
BORDER  = "#3A3A5C"
ERROR   = "#C0392B"

class LoginApp:

    def __init__(self, root):
        self.root = root
        self.root.title("THE BANK OF ODOTEH — Login")
        self.root.geometry("360x460")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.mode = "login"
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="🏦", bg=BG,
                 font=("Helvetica", 36)).pack(pady=(30, 0))
        tk.Label(self.root, text="THE BANK OF ODOTEH", bg=BG,
                 fg=TEXT, font=("Helvetica", 20, "bold")).pack()
        self.subtitle = tk.Label(self.root,
                 text="Sign in to your account",
                 bg=BG, fg=SUBTEXT, font=("Helvetica", 10))
        self.subtitle.pack(pady=(2, 20))

        form = tk.Frame(self.root, bg=BG, padx=30)
        form.pack(fill="x")

        tk.Label(form, text="USERNAME", bg=BG, fg=SUBTEXT,
                 font=("Helvetica", 9)).pack(anchor="w")
        self.username_entry = tk.Entry(form,
                 font=("Helvetica", 12), bg=PANEL, fg=TEXT,
                 insertbackground=TEXT, relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=ACCENT)
        self.username_entry.pack(fill="x", ipady=8, pady=(2, 12))

        tk.Label(form, text="PASSWORD", bg=BG, fg=SUBTEXT,
                 font=("Helvetica", 9)).pack(anchor="w")
        self.password_entry = tk.Entry(form,
                 font=("Helvetica", 12), bg=PANEL, fg=TEXT,
                 insertbackground=TEXT, relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=ACCENT,
                 show="•")
        self.password_entry.pack(fill="x", ipady=8, pady=(2, 4))

        self.error_label = tk.Label(form, text="",
                 bg=BG, fg=ERROR, font=("Helvetica", 9))
        self.error_label.pack(anchor="w", pady=(0, 8))

        self.main_btn = tk.Button(form,
                 text="Sign In", command=self.submit,
                 bg=ACCENT, fg="white",
                 font=("Helvetica", 11, "bold"),
                 relief="flat", bd=0, pady=10,
                 cursor="hand2",
                 activebackground=ACCENT,
                 activeforeground="white")
        self.main_btn.pack(fill="x", pady=(0, 12))

        self.root.bind("<Return>", lambda e: self.submit())

        self.toggle_btn = tk.Button(form,
                 text="Don't have an account? Register",
                 command=self.toggle_mode,
                 bg=BG, fg="#7F77DD",
                 font=("Helvetica", 9),
                 relief="flat", bd=0,
                 cursor="hand2",
                 activebackground=BG,
                 activeforeground="#7F77DD")
        self.toggle_btn.pack()

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.subtitle.config(text="Create a new account")
            self.main_btn.config(text="Register")
            self.toggle_btn.config(text="Already have an account? Sign In")
        else:
            self.mode = "login"
            self.subtitle.config(text="Sign in to your account")
            self.main_btn.config(text="Sign In")
            self.toggle_btn.config(text="Don't have an account? Register")
        self.error_label.config(text="")

    def submit(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if self.mode == "register":
            ok, msg = register(username, password)
            if ok:
                messagebox.showinfo("Success", msg)
                self.toggle_mode()
            else:
                self.error_label.config(text=msg)
        else:
            if login(username, password):
                self.root.destroy()
                self.open_bank_app(username)
            else:
                self.error_label.config(
                    text="Incorrect username or password.")

    def open_bank_app(self, username):
        from ui import BankApp
        new_root = tk.Tk()
        BankApp(new_root, username)
        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()