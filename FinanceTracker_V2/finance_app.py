# finance_app.py

import sqlite3
import datetime

class FinanceApp:
    def __init__(self, db_name='finance_app.db'):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Balance (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            balance REAL NOT NULL DEFAULT 0,  
            daily_spendings_total REAL NOT NULL DEFAULT 0,
            weekly_spendings_total REAL NOT NULL DEFAULT 0,
            monthly_spendings_total REAL NOT NULL DEFAULT 0,
            yearly_spendings_total REAL NOT NULL DEFAULT 0,
            current_investments REAL NOT NULL DEFAULT 0
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transac (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            product TEXT,
            description TEXT,
            spending_type TEXT NOT NULL CHECK (
                spending_type IN ('Earning Money', 'Investment', 'Spending', 'Bills')
            ),
            FOREIGN KEY (account_id) REFERENCES Balance(account_id)
        );
        ''')

        conn.commit()
        conn.close()

    def log_transaction(self, account_id, spending_type, transaction_amount, product, description):
        transaction_time = datetime.datetime.now()
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO Transac (account_id, amount, date, product, description, spending_type)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (account_id, transaction_amount, transaction_time, product, description, spending_type))
            conn.commit()
            print("Transaction logged successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred while logging the transaction: {e}")
        finally:
            conn.close()

    def get_balance_data(self, account_id, column):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f'''
            SELECT {column} FROM Balance WHERE account_id = ?
            ''', (account_id,))
            result = cursor.fetchone()
            if not result:
                print("Account ID not found.")
                return None
            else:
                return result[0]
        except sqlite3.Error as e:
            print(f"An error occurred while fetching balance data: {e}")
            return None 
        finally:
            conn.close()

    def update_balance(self, account_id, new_balance):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('UPDATE Balance SET balance = ? WHERE account_id = ?', (new_balance, account_id))
            conn.commit()
            print("Balance updated successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred while updating balance: {e}")
        finally:
            conn.close()

    def update_spending_totals(self, account_id):
        self.update_daily_spending_total(account_id)
        self.update_weekly_spending_total(account_id)
        self.update_monthly_spending_total(account_id)
        self.update_yearly_spending_total(account_id)

    def update_daily_spending_total(self, account_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            SELECT SUM(-amount)
            FROM Transac
            WHERE account_id = ? AND spending_type IN ('Spending', 'Bills', 'Investment')
              AND DATE(date) = DATE('now')
            ''', (account_id,))
            daily_total = cursor.fetchone()[0] or 0
            cursor.execute('UPDATE Balance SET daily_spendings_total = ? WHERE account_id = ?', (daily_total, account_id))
            conn.commit()
            print("Daily spending total updated successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred while updating daily spending total: {e}")
        finally:
            conn.close()

    def update_weekly_spending_total(self, account_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            SELECT SUM(-amount)
            FROM Transac
            WHERE account_id = ? AND spending_type IN ('Spending', 'Bills', 'Investment')
              AND strftime('%Y-%W', date) = strftime('%Y-%W', 'now')
            ''', (account_id,))
            weekly_total = cursor.fetchone()[0] or 0
            cursor.execute('UPDATE Balance SET weekly_spendings_total = ? WHERE account_id = ?', (weekly_total, account_id))
            conn.commit()
            print("Weekly spending total updated successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred while updating weekly spending total: {e}")
        finally:
            conn.close()

    def update_monthly_spending_total(self, account_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            SELECT SUM(-amount)
            FROM Transac
            WHERE account_id = ? AND spending_type IN ('Spending', 'Bills', 'Investment')
              AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
            ''', (account_id,))
            monthly_total = cursor.fetchone()[0] or 0
            cursor.execute('UPDATE Balance SET monthly_spendings_total = ? WHERE account_id = ?', (monthly_total, account_id))
            conn.commit()
            print("Monthly spending total updated successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred while updating monthly spending total: {e}")
        finally:
            conn.close()

    def update_yearly_spending_total(self, account_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            SELECT SUM(-amount)
            FROM Transac
            WHERE account_id = ? AND spending_type IN ('Spending', 'Bills', 'Investment')
              AND strftime('%Y', date) = strftime('%Y', 'now')
            ''', (account_id,))
            yearly_total = cursor.fetchone()[0] or 0
            cursor.execute('UPDATE Balance SET yearly_spendings_total = ? WHERE account_id = ?', (yearly_total, account_id))
            conn.commit()
            print("Yearly spending total updated successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred while updating yearly spending total: {e}")
        finally:
            conn.close()

    def update_current_investments(self, account_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            SELECT SUM(-amount)
            FROM Transac
            WHERE account_id = ? AND spending_type = 'Investment'
            ''', (account_id,))
            investments_total = cursor.fetchone()[0] or 0
            cursor.execute('UPDATE Balance SET current_investments = ? WHERE account_id = ?', (investments_total, account_id))
            conn.commit()
            print("Current investments updated successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred while updating current investments: {e}")
        finally:
            conn.close()

    def create_account(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Balance (balance) VALUES (0)')
            conn.commit()
            account_id = cursor.lastrowid
            print(f"Account created with ID: {account_id}")
            return account_id
        except sqlite3.Error as e:
            print(f"An error occurred while creating an account: {e}")
            return None
        finally:
            conn.close()

    def process_transaction(self, account_id, spending_type, transaction_amount, product, description):
        current_balance = self.get_balance_data(account_id, 'balance')
        if current_balance is None:
            print("Account ID not found.")
            return

        if spending_type == 'Earning Money':
            amount = transaction_amount  # Positive amount
            current_balance += transaction_amount

        elif spending_type in ('Investment', 'Spending', 'Bills'):
            amount = -transaction_amount  # Negative amount
            current_balance -= transaction_amount

        else:
            print("Invalid spending type.")
            return

        # Update the balance in the database
        self.update_balance(account_id, current_balance)

        # Log the transaction
        self.log_transaction(account_id, spending_type, amount, product, description)

        # Update all spending totals
        self.update_spending_totals(account_id)

        # Update current investments if the transaction is an investment
        if spending_type == 'Investment':
            self.update_current_investments(account_id)

        print(f"Your updated balance is: {current_balance}")

    def get_latest_transactions(self, account_id, limit=5):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            SELECT date, spending_type, amount, product, description
            FROM Transac
            WHERE account_id = ?
            ORDER BY date DESC
            LIMIT ?
            ''', (account_id, limit))
            transactions = cursor.fetchall()
            return transactions
        except sqlite3.Error as e:
            print(f"An error occurred while fetching transactions: {e}")
            return []
        finally:
            conn.close()
