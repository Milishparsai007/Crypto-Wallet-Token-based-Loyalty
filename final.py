import ecdsa
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog

class BlockchainAccount:
    def __init__(self, username):
        self.username = username
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()
        self.address = self.generate_address()
        self.balance = 0.0001  # Initial balance set to 0.0001 cryptos
        self.tokens_earned = 0  # Tokens earned
        self.transaction_count = 0  # Number of transactions
        self.exchange_history = []  # Stores e-waste exchange history

    def generate_private_key(self):
        return ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    def generate_public_key(self):
        return self.private_key.get_verifying_key()

    def generate_address(self):
        public_key_bytes = self.public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes).digest()
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
        return ripemd160_bpk.hex()

    def get_account_details(self):
        return {
            'username': self.username,
            'balance': self.balance,
            'tokens_earned': self.tokens_earned,
            'transaction_count': self.transaction_count,
            'exchange_history': self.exchange_history
        }

    def exchange_ewaste(self, weight):
        tokens = weight * 0.5  # 1kg = 0.5 tokens
        self.tokens_earned += tokens
        exchange_entry = f"{weight} kg → {tokens:.2f} tokens"
        self.exchange_history.append(exchange_entry)
        return tokens

    def redeem_tokens(self, tokens_to_redeem):
        if tokens_to_redeem <= self.tokens_earned and tokens_to_redeem >= 1:
            cryptos_gained = tokens_to_redeem * 0.0001  # 1 token = 0.0001 cryptos
            self.tokens_earned -= tokens_to_redeem
            self.balance += cryptos_gained
            return cryptos_gained
        return None

class BlockchainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain & E-Waste Management")
        self.root.geometry("500x500")

        self.accounts = []  # Store user accounts (RAM only)

        self.create_widgets()

    def create_widgets(self):
        self.description_label = tk.Label(self.root, text="Blockchain & E-Waste Management", font=("Arial", 14))
        self.description_label.pack(pady=10)

        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.create_account)
        self.create_account_button.pack(pady=5)

        self.user_details_button = tk.Button(self.root, text="Check User Details", command=self.check_user_details)
        self.user_details_button.pack(pady=5)

        self.transfer_button = tk.Button(self.root, text="Transfer Cryptos", command=self.transfer_cryptos)
        self.transfer_button.pack(pady=5)

        self.check_balance_button = tk.Button(self.root, text="Check Balance", command=self.check_balance)
        self.check_balance_button.pack(pady=5)

        self.exchange_button = tk.Button(self.root, text="Exchange E-Waste", command=self.exchange_ewaste)
        self.exchange_button.pack(pady=5)

        self.history_button = tk.Button(self.root, text="Exchange History", command=self.view_exchange_history)
        self.history_button.pack(pady=5)

        self.redeem_tokens_button = tk.Button(self.root, text="Redeem Tokens", command=self.redeem_tokens)
        self.redeem_tokens_button.pack(pady=5)

        # New button to view tokens earned
        self.view_tokens_button = tk.Button(self.root, text="View Tokens Earned", command=self.view_tokens_earned)
        self.view_tokens_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def create_account(self):
        username = simpledialog.askstring("Input", "Enter username:")
        if username:
            if self.find_account(username):
                messagebox.showerror("Error", "User already exists!")
            else:
                account = BlockchainAccount(username)
                self.accounts.append(account)
                messagebox.showinfo("Account Created", f"Account created!\nUsername: {username}\nBalance: 0.0001 cryptos")

    def find_account(self, username):
        for account in self.accounts:
            if account.username == username:
                return account
        return None

    def transfer_cryptos(self):
        sender_username = simpledialog.askstring("Input", "Enter sender's username:")
        recipient_username = simpledialog.askstring("Input", "Enter recipient's username:")
        amount = simpledialog.askfloat("Input", "Enter amount to transfer:")

        sender = self.find_account(sender_username)
        recipient = self.find_account(recipient_username)

        if sender and recipient and amount:
            if sender.balance >= amount:
                sender.balance -= amount
                recipient.balance += amount
                sender.transaction_count += 1
                messagebox.showinfo("Transfer Successful", f"Transferred {amount} cryptos from {sender_username} to {recipient_username}.")
            else:
                messagebox.showerror("Error", "Insufficient balance!")
        else:
            messagebox.showerror("Error", "Invalid sender, recipient, or amount.")

    def check_balance(self):
        username = simpledialog.askstring("Input", "Enter username:")
        account = self.find_account(username)
        if account:
            messagebox.showinfo("Balance", f"{username}'s balance: {account.balance:.6f} cryptos")
        else:
            messagebox.showerror("Error", "Account not found.")

    def check_user_details(self):
        username = simpledialog.askstring("Input", "Enter username:")
        account = self.find_account(username)
        if account:
            details = account.get_account_details()
            messagebox.showinfo("User Details", f"Username: {details['username']}\n"
                                                f"Balance: {details['balance']:.6f} cryptos\n"
                                                f"Tokens Earned: {details['tokens_earned']:.2f}\n"
                                                f"Transaction Count: {details['transaction_count']}")
        else:
            messagebox.showerror("Error", "Account not found.")

    def exchange_ewaste(self):
        username = simpledialog.askstring("Input", "Enter username:")
        account = self.find_account(username)
        if account:
            weight = simpledialog.askfloat("Input", "Enter e-waste weight (kg):")
            if weight and weight > 0:
                tokens = account.exchange_ewaste(weight)
                messagebox.showinfo("Exchange Successful", f"Received {tokens:.2f} tokens for {weight} kg e-waste!")
        else:
            messagebox.showerror("Error", "Create an account first!")

    def view_exchange_history(self):
        username = simpledialog.askstring("Input", "Enter username:")
        account = self.find_account(username)
        if account:
            history = "\n".join(account.exchange_history) if account.exchange_history else "No exchanges yet."
            messagebox.showinfo("Exchange History", history)
        else:
            messagebox.showerror("Error", "Create an account first!")

    def redeem_tokens(self):
        username = simpledialog.askstring("Input", "Enter username:")
        account = self.find_account(username)
        if account:
            tokens_to_redeem = simpledialog.askinteger("Input", f"Enter tokens to redeem (Max: {account.tokens_earned:.2f}):")
            if tokens_to_redeem:
                cryptos_gained = account.redeem_tokens(tokens_to_redeem)
                if cryptos_gained:
                    messagebox.showinfo("Redeemed", f"Converted {tokens_to_redeem} tokens → {cryptos_gained:.6f} cryptos!")
                else:
                    messagebox.showerror("Error", "Invalid token amount!")
        else:
            messagebox.showerror("Error", "Account not found!")

    def view_tokens_earned(self):
        username = simpledialog.askstring("Input", "Enter username:")
        account = self.find_account(username)
        if account:
            messagebox.showinfo("Tokens Earned", f"{username} has earned {account.tokens_earned:.2f} tokens.")
        else:
            messagebox.showerror("Error", "Account not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()
