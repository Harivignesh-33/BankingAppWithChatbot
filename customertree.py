from tkinter import ttk, messagebox
import tkinter as tk
import sqlite3
import adminpage


class CustomerTree:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin - Customer Details")
        self.root.geometry("1100x500")
        self.root.configure(bg="#f0f0f0")
        self.root.state("zoomed")

        # Title Label
        title = tk.Label(self.root, text="Customer Details", font=("Arial", 18, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Frame for Search and Buttons
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=10)

        tk.Label(top_frame, text="Search:", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(top_frame, textvariable=self.search_var, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(top_frame, text="Search", font=("Arial", 12), command=self.search_customer, bg="#4CAF50", fg="white")
        search_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = tk.Button(top_frame, text="Refresh", font=("Arial", 12), command=self.view, bg="#2196F3", fg="white")
        refresh_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(top_frame, text="Delete", font=("Arial", 12), command=self.delete_customer, bg="#F44336", fg="white")
        delete_btn.pack(side=tk.LEFT, padx=5)

        back_btn = tk.Button(top_frame, text="Back", font=("Arial", 12), command=self.go_back, bg="#FF9800", fg="white")
        back_btn.pack(side=tk.LEFT, padx=5)

        # Treeview for Data
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10"), show='headings')

        headings = ["Account Number", "Name", "Address", "Contact", "E-Mail", "Adhar", "Pancard No", "Bank Name", "IFSC Code", "Balance Amount"]
        for i, text in enumerate(headings, 1):
            self.tree.heading(f"# {i}", text=text)
            self.tree.column(f"# {i}", width=120, anchor=tk.CENTER)

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
        cursor.execute("SELECT acno, nam, addr, con, mail, adhar, pan, bank, ifsc, amt FROM cusdetails")
        rows = cursor.fetchall()
        con.close()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def search_customer(self):
        search_text = self.search_var.get().strip()
        if not search_text:
            messagebox.showwarning("Warning", "Enter a name or account number to search.")
            return

        con = self.connect_db()
        cursor = con.cursor()
        cursor.execute(
            "SELECT acno, nam, addr, con, mail, adhar, pan, bank, ifsc, amt FROM cusdetails WHERE nam LIKE ? OR acno LIKE ?",
            (f"%{search_text}%", f"%{search_text}%"))
        rows = cursor.fetchall()
        con.close()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def delete_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a customer to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if not confirm:
            return

        item = self.tree.item(selected_item)
        acno = item['values'][0]

        con = self.connect_db()
        cursor = con.cursor()
        cursor.execute("DELETE FROM cusdetails WHERE acno = ?", (acno,))
        con.commit()
        con.close()

        self.tree.delete(selected_item)
        messagebox.showinfo("Success", "Customer deleted successfully!")

    def go_back(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerTree(root)
    root.mainloop()
