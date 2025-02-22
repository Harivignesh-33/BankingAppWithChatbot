from tkinter import ttk, messagebox
import tkinter as tk
import sqlite3


class CustomerTransactionTree:
    def __init__(self, root, acc_no):
        self.root = root
        self.root.title("Your Transaction History")
        self.root.geometry("800x450")
        self.root.configure(bg="#f0f0f0")

        self.acc_no = str(acc_no).strip()  # Ensure acc_no is always a string

        # Title Label
        title = tk.Label(self.root, text="Transaction History", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Balance Display Label
        self.balance_label = tk.Label(self.root, text="Balance: ₹0.00", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.balance_label.pack(pady=5)

        # Treeview Frame
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("Date", "Type", "Amount"), show='headings')

        self.tree.heading("Date", text="Date")
        self.tree.heading("Type", text="Transaction Type")
        self.tree.heading("Amount", text="Amount")

        self.tree.column("Date", width=100, anchor=tk.CENTER)
        self.tree.column("Type", width=150, anchor=tk.CENTER)
        self.tree.column("Amount", width=100, anchor=tk.CENTER)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Close Button
        close_button = tk.Button(self.root, text="Close", font=("Arial", 12, "bold"), bg="#E74C3C", fg="white",
                                 width=15, command=self.close_window)
        close_button.pack(pady=10)

        # ✅ Debug: Print account number before fetching transactions
        print(f"🔍 Fetching transactions for Account No: {self.acc_no}")

        # Auto-Refresh Transactions & Balance
        self.update_data()

    def connect_db(self):
        """Establish a database connection safely."""
        try:
            return sqlite3.connect("bank.db")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {str(e)}")
            return None

    def view(self):
        """Fetch and display transactions of the logged-in user."""
        con = self.connect_db()
        if not con:
            return  # Prevent execution if DB connection failed

        cursor = con.cursor()
        try:
            cursor.execute("SELECT dat, tt, amt FROM trans WHERE acno = ?", (self.acc_no,))
            rows = cursor.fetchall()

            # ✅ Debug: Check if any transactions exist
            if not rows:
                print("⚠️ No transactions found for this account.")

            self.tree.delete(*self.tree.get_children())  # Clear previous data

            for index, row in enumerate(rows):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", tk.END, values=row, tags=(tag,))

            self.tree.tag_configure("evenrow", background="#EAF6F6")  # Light blue
            self.tree.tag_configure("oddrow", background="#FFFFFF")   # White

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching transactions: {str(e)}")
        finally:
            con.close()

    def update_balance(self):
        """Calculate balance dynamically from transactions."""
        con = self.connect_db()
        if not con:
            return  # Prevent execution if DB connection failed

        cursor = con.cursor()
        try:
            cursor.execute(
                "SELECT SUM(CASE WHEN tt = 'Deposit' THEN amt ELSE -amt END) FROM trans WHERE acno = ?",
                (self.acc_no,))
            balance = cursor.fetchone()[0]

            # ✅ Ensure balance is not None
            balance_amt = balance if balance is not None else 0.00
            self.balance_label.config(text=f"Balance: ₹{balance_amt:,.2f}")

            # ✅ Debug: Print balance
            print(f"💰 Updated Balance: ₹{balance_amt:,.2f}")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching balance: {str(e)}")
        finally:
            con.close()

    def update_data(self):
        """Refresh transactions and balance every 5 seconds."""
        self.view()
        self.update_balance()
        self.root.after(5000, self.update_data)  # Auto-refresh every 5 seconds

    def close_window(self):
        """Close the transaction window properly."""
        self.root.destroy()


# ✅ Run Standalone Test (Replace with real account number)
if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerTransactionTree(root, "1000000001")  # Replace with actual account number
    root.mainloop()
