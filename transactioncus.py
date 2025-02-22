import customtkinter as ctk
import sqlite3
import datetime
from tkinter import messagebox


class transac(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Transaction Page")

        # 🆕 Default Windows Min/Max/Close buttons enabled
        self.geometry("1024x768")  # Initial size
        self.state('zoomed')  # Open in maximized mode
        self.attributes('-topmost', True)
        self.configure(bg="#F8F9FA")

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        ctk.CTkLabel(main_frame, text="Transaction", font=("Arial", 25, "bold"), text_color="#333").pack(pady=10)

        form_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
        form_frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.acno = ctk.CTkEntry(form_frame, placeholder_text="Account Number", width=300)
        self.acno.grid(row=0, column=1, pady=10, padx=10)

        self.nam = ctk.CTkEntry(form_frame, placeholder_text="Name", width=300)
        self.nam.grid(row=1, column=1, pady=10, padx=10)
        self.nam.bind("<FocusIn>", self.fetch_name)

        self.dat = ctk.CTkEntry(form_frame, width=300)
        self.dat.grid(row=2, column=1, pady=10, padx=10)
        self.dat.insert(0, str(datetime.date.today()))

        self.tt = ctk.CTkComboBox(form_frame, values=["Deposit", "Withdraw"], width=300)
        self.tt.grid(row=3, column=1, pady=10, padx=10)

        self.amt = ctk.CTkEntry(form_frame, placeholder_text="Amount", width=300)
        self.amt.grid(row=4, column=1, pady=10, padx=10)

        button_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Submit", command=self.save, fg_color="#1ABC9C", width=150).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Clear", command=self.clear, fg_color="#E74C3C", width=150).grid(row=0, column=1, padx=10)
        ctk.CTkButton(button_frame, text="Close", command=self.destroy, fg_color="#3498DB", width=150).grid(row=0, column=2, padx=10)

    def save(self):
        acno = self.acno.get()
        name = self.nam.get()
        date = self.dat.get()
        trans_type = self.tt.get()
        amount = self.amt.get()

        if not acno or not name or not amount or trans_type == "Select Transaction Type":
            messagebox.showwarning("Input Error", "Please fill all fields correctly", parent=self)
            return

        try:
            amount = int(amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number", parent=self)
            return

        with sqlite3.connect("bank.db") as con:
            cur = con.cursor()
            if trans_type == "Deposit":
                cur.execute('INSERT INTO trans (acno, nam, dat, tt, amt) VALUES (?, ?, ?, ?, ?)',
                            (acno, name, date, trans_type, amount))
                cur.execute('UPDATE cusdetails SET amt = amt + ? WHERE acno = ?', (amount, acno))
            else:
                cur.execute("SELECT amt FROM cusdetails WHERE acno = ?", (acno,))
                result = cur.fetchone()
                if result and result[0] >= amount:
                    cur.execute('INSERT INTO trans (acno, nam, dat, tt, amt) VALUES (?, ?, ?, ?, ?)',
                                (acno, name, date, trans_type, amount))
                    cur.execute('UPDATE cusdetails SET amt = amt - ? WHERE acno = ?', (amount, acno))
                else:
                    messagebox.showwarning("Transaction Error", "Insufficient Balance", parent=self)
                    return
            con.commit()
            messagebox.showinfo("Success", "Transaction Completed Successfully", parent=self)
        self.clear()

    def fetch_name(self, event):
        acno = self.acno.get()
        if not acno:
            return
        with sqlite3.connect("bank.db") as con:
            cur = con.cursor()
            cur.execute("SELECT nam FROM cusdetails WHERE acno = ?", (acno,))
            result = cur.fetchone()
            if result:
                self.nam.delete(0, 'end')
                self.nam.insert(0, result[0])

    def clear(self):
        self.acno.delete(0, 'end')
        self.nam.delete(0, 'end')
        self.tt.set("Select Transaction Type")
        self.amt.delete(0, 'end')
