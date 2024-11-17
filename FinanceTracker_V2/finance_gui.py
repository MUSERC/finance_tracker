# finance_gui.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from finance_app import FinanceApp

class FinanceAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Application")
        self.app = FinanceApp()
        self.account_id = None

        # Apply a modern theme
        style = ttk.Style('cosmo')  # Choose from 'cosmo', 'darkly', 'flatly', 'journal', etc.
        self.create_widgets()

    def create_widgets(self):
        # Account Frame
        account_frame = ttk.Frame(self.root, padding=10)
        account_frame.pack(fill='x')

        ttk.Label(account_frame, text="Do you have an account?", font='Helvetica 12 bold').pack(side='left')
        self.account_var = ttk.StringVar(value='Y')
        ttk.Radiobutton(account_frame, text="Yes", variable=self.account_var, value='Y', command=self.toggle_account_entry).pack(side='left', padx=5)
        ttk.Radiobutton(account_frame, text="No", variable=self.account_var, value='N', command=self.toggle_account_entry).pack(side='left', padx=5)

        self.account_entry = ttk.Entry(account_frame)
        self.account_entry.pack(side='left', padx=5)
        self.account_entry.insert(0, "Enter Account ID")

        # Separator
        ttk.Separator(self.root).pack(fill='x', pady=10)

        # Transaction Frame
        transaction_frame = ttk.Frame(self.root, padding=10)
        transaction_frame.pack(fill='x')

        ttk.Label(transaction_frame, text="Type of Transaction:", font='Helvetica 10 bold').grid(row=0, column=0, sticky='e', pady=5)
        self.spending_type_var = ttk.StringVar()
        spending_types = ['Earning Money', 'Investment', 'Spending', 'Bills']
        self.spending_type_menu = ttk.OptionMenu(transaction_frame, self.spending_type_var, *spending_types)
        self.spending_type_menu.grid(row=0, column=1, sticky='w', pady=5)

        ttk.Label(transaction_frame, text="Amount:", font='Helvetica 10 bold').grid(row=1, column=0, sticky='e', pady=5)
        self.amount_entry = ttk.Entry(transaction_frame)
        self.amount_entry.grid(row=1, column=1, sticky='w', pady=5)

        ttk.Label(transaction_frame, text="Product/Source:", font='Helvetica 10 bold').grid(row=2, column=0, sticky='e', pady=5)
        self.product_entry = ttk.Entry(transaction_frame)
        self.product_entry.grid(row=2, column=1, sticky='w', pady=5)

        ttk.Label(transaction_frame, text="Description:", font='Helvetica 10 bold').grid(row=3, column=0, sticky='e', pady=5)
        self.description_entry = ttk.Entry(transaction_frame)
        self.description_entry.grid(row=3, column=1, sticky='w', pady=5)

        # Buttons
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill='x')

        self.submit_button = ttk.Button(button_frame, text="Submit Transaction", command=self.submit_transaction, style='success.TButton')
        self.submit_button.pack(side='left', padx=5)

        self.view_balance_button = ttk.Button(button_frame, text="View Balance", command=self.view_balance, style='info.TButton')
        self.view_balance_button.pack(side='left', padx=5)

        self.quit_button = ttk.Button(button_frame, text="Quit", command=self.root.quit, style='danger.TButton')
        self.quit_button.pack(side='right', padx=5)

        # Latest Transactions Frame
        self.transactions_frame = ttk.Frame(self.root, padding=10)
        self.transactions_frame.pack(fill='both', expand=True)

        ttk.Label(self.transactions_frame, text="Latest Transactions:", font='Helvetica 12 bold').pack(anchor='w')

        # Treeview for displaying transactions
        columns = ('Date', 'Type', 'Amount', 'Product', 'Description')
        self.transactions_tree = ttk.Treeview(self.transactions_frame, columns=columns, show='headings')

        for col in columns:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, anchor='center')

        self.transactions_tree.pack(fill='both', expand=True)

    def toggle_account_entry(self):
        if self.account_var.get() == 'Y':
            self.account_entry.config(state='normal')
            self.account_entry.delete(0, ttk.END)
            self.account_entry.insert(0, "Enter Account ID")
        else:
            self.account_entry.config(state='disabled')
            self.account_entry.delete(0, ttk.END)

    def submit_transaction(self):
        if self.account_var.get() == 'Y':
            try:
                account_id = int(self.account_entry.get())
                self.account_id = account_id
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid Account ID.")
                return
        else:
            self.account_id = self.app.create_account()
            messagebox.showinfo("Account Created", f"Your new account ID is: {self.account_id}")

        spending_type = self.spending_type_var.get()
        if not spending_type:
            messagebox.showerror("Invalid Input", "Please select a transaction type.")
            return

        amount_text = self.amount_entry.get()
        if not amount_text:
            messagebox.showerror("Invalid Input", "Please enter an amount.")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive number for the amount.")
            return

        product = self.product_entry.get()
        description = self.description_entry.get()

        self.app.process_transaction(self.account_id, spending_type, amount, product, description)
        messagebox.showinfo("Transaction Successful", f"Transaction processed for Account ID: {self.account_id}")

        # Clear fields after submission
        self.amount_entry.delete(0, ttk.END)
        self.product_entry.delete(0, ttk.END)
        self.description_entry.delete(0, ttk.END)

        # Update the latest transactions
        self.update_transactions()

    def view_balance(self):
        if self.account_var.get() == 'Y':
            try:
                account_id = int(self.account_entry.get())
                self.account_id = account_id  # Update the stored account_id
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid Account ID.")
                return
        else:
            messagebox.showerror("Account Not Found", "You need an account to view balance.")
            return

        balance = self.app.get_balance_data(account_id, 'balance')
        daily_total = self.app.get_balance_data(account_id, 'daily_spendings_total')
        weekly_total = self.app.get_balance_data(account_id, 'weekly_spendings_total')
        monthly_total = self.app.get_balance_data(account_id, 'monthly_spendings_total')
        yearly_total = self.app.get_balance_data(account_id, 'yearly_spendings_total')
        investments = self.app.get_balance_data(account_id, 'current_investments')

        if balance is None:
            messagebox.showerror("Account Not Found", "The account ID you entered does not exist.")
            return

        balance_info = (
            f"Balance: {balance:.2f}\n"
            f"Today's Spending: {daily_total:.2f}\n"
            f"This Week's Spending: {weekly_total:.2f}\n"
            f"This Month's Spending: {monthly_total:.2f}\n"
            f"This Year's Spending: {yearly_total:.2f}\n"
            f"Current Investments: {investments:.2f}"
        )
        messagebox.showinfo("Balance Information", balance_info)

        # Update the latest transactions
        self.update_transactions()

    def update_transactions(self):
        # Clear the existing transactions
        for row in self.transactions_tree.get_children():
            self.transactions_tree.delete(row)

        # Get the latest transactions
        transactions = self.app.get_latest_transactions(self.account_id)

        # Insert the transactions into the treeview
        for trans in transactions:
            date_str = trans[0]
            spending_type = trans[1]
            amount = trans[2]
            product = trans[3]
            description = trans[4]
            self.transactions_tree.insert('', 'end', values=(date_str, spending_type, f"{amount:.2f}", product, description))

if __name__ == "__main__":
    app = ttk.Window("Finance Application", themename="cosmo", size=(600, 600))
    app_gui = FinanceAppGUI(app)
    app.mainloop()
