from tkinter import ttk, messagebox
import tkinter as tk
import sqlite3
import adminpage


class TransactionTree:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin - Transaction Details")
        self.root.geometry("1100x500")
        self.root.configure(bg="#f0f0f0")
        self.root.state("zoomed")

        # Title Label
        title = tk.Label(self.root, text="Transaction Details", font=("Arial", 18, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Frame for Search and Buttons
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=10)

        tk.Label(top_frame, text="Search:", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(top_frame, textvariable=self.search_var, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(top_frame, text="Search", font=("Arial", 12), command=self.search_transaction, bg="#4CAF50", fg="white")
        search_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = tk.Button(top_frame, text="Refresh", font=("Arial", 12), command=self.view, bg="#2196F3", fg="white")
        refresh_btn.pack(side=tk.LEFT, padx=5)

        back_btn = tk.Button(top_frame, text="Back", font=("Arial", 12), command=self.go_back, bg="#FF9800", fg="white")
        back_btn.pack(side=tk.LEFT, padx=5)

        # Treeview for Data
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, columns=("c1", "c2", "c3", "c4", "c5"), show='headings')

        headings = ["Account Number", "Name", "Date", "Transaction Type", "Transaction Amount"]
        for i, text in enumerate(headings, 1):
            self.tree.heading(f"#{i}", text=text)
            self.tree.column(f"#{i}", width=150, anchor=tk.CENTER)

        # Scrollbars
        scrollbar_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_y = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(xscroll=scrollbar_x.set, yscroll=scrollbar_y.set)

        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Load Data
        self.view()

    def connect_db(self):
        return sqlite3.connect('bank.db')

    def view(self):
        con = self.connect_db()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM trans")
        rows = cursor.fetchall()
        con.close()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def search_transaction(self):
        search_text = self.search_var.get().strip()
        if not search_text:
            messagebox.showwarning("Warning", "Enter an account number or name to search.")
            return

        con = self.connect_db()
        cursor = con.cursor()
        cursor.execute(
            "SELECT * FROM trans WHERE acno LIKE ? OR nam LIKE ?",
            (f"%{search_text}%", f"%{search_text}%"))
        rows = cursor.fetchall()
        con.close()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    # def go_back(self):
    #     self.root.destroy()
    #     adminpage.AdminPage()

    def go_back(self):
        """Closes transaction page without affecting the Admin Page"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TransactionTree(root)
    root.mainloop()
