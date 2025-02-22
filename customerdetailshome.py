import customtkinter as ctk
import sqlite3
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class CustomerRegistration:
    def __init__(self, root):
        self.root = root
        self.root.state("zoomed")
        self.root.title("Customer Registration")

        # Outer Frame
        self.outer_frame = ctk.CTkFrame(self.root, fg_color="#E0E0E0")
        self.outer_frame.pack(expand=True, fill="both", padx=50, pady=50)

        form_title = ctk.CTkLabel(self.outer_frame, text="Customer Registration", font=("Arial", 26, "bold"))
        form_title.pack(pady=(25, 0))

        # Inner Frame
        self.inner_frame = ctk.CTkFrame(self.outer_frame, width=800, height=550, corner_radius=15)
        self.inner_frame.pack(pady=20, padx=30, ipadx=20, ipady=20)

        self.entries = {}

        # **Bank Name & IFSC Code**
        bank_label = ctk.CTkLabel(self.inner_frame, text="Bank Name:", font=("Arial", 16))
        bank_label.grid(row=0, column=0, padx=15, pady=(25, 12), sticky="e")

        self.bank_options = [
            "Select the Bank", "Union Bank of India", "State Bank of India", "Canara Bank", "Indian Overseas Bank",
            "City Union Bank", "Axis Bank", "ICICI Bank", "HDFC Bank", "Bank of Baroda", "Punjab National Bank",
            "IDBI Bank", "Kotak Mahindra Bank", "Yes Bank", "IndusInd Bank", "Federal Bank"
        ]

        self.bank_dropdown = ctk.CTkComboBox(self.inner_frame, values=self.bank_options, width=320, height=40, state="readonly")
        self.bank_dropdown.set("Select the Bank")
        self.bank_dropdown.grid(row=0, column=1, padx=15, pady=(25, 12), sticky="w")

        ifsc_label = ctk.CTkLabel(self.inner_frame, text="IFSC Code:", font=("Arial", 16))
        ifsc_label.grid(row=0, column=2, padx=15, pady=(25, 12), sticky="e")

        ifsc_entry = ctk.CTkEntry(self.inner_frame, width=320, height=40, corner_radius=8)
        ifsc_entry.grid(row=0, column=3, padx=15, pady=(25, 12), sticky="w")
        self.entries["IFSC Code"] = ifsc_entry

        # **Account Number & Balance**
        acno_label = ctk.CTkLabel(self.inner_frame, text="Account No:", font=("Arial", 16))
        acno_label.grid(row=1, column=0, padx=15, pady=12, sticky="e")

        acno_entry = ctk.CTkEntry(self.inner_frame, width=320, height=40, corner_radius=8)
        acno_entry.grid(row=1, column=1, padx=15, pady=12, sticky="w")
        acno_entry.configure(state="disabled")
        self.entries["Account Number"] = acno_entry

        balance_label = ctk.CTkLabel(self.inner_frame, text="Balance:", font=("Arial", 16))
        balance_label.grid(row=1, column=2, padx=15, pady=12, sticky="e")

        balance_entry = ctk.CTkEntry(self.inner_frame, width=320, height=40, corner_radius=8)
        balance_entry.insert(0, "1000.00")
        balance_entry.configure(state="disabled")
        balance_entry.grid(row=1, column=3, padx=15, pady=12, sticky="w")
        self.entries["Balance"] = balance_entry

        # **Other Fields**
        fields = [
            ("Name", "Contact"),
            ("Address", "Aadhar No"),
            ("E-Mail", "Pancard No"),
            ("User Name", "Password")
        ]

        for row, (left_field, right_field) in enumerate(fields, start=2):
            left_label = ctk.CTkLabel(self.inner_frame, text=f"{left_field}:", font=("Arial", 16))
            left_label.grid(row=row, column=0, padx=15, pady=12, sticky="e")

            left_entry = ctk.CTkEntry(self.inner_frame, width=320, height=40, corner_radius=8)
            if left_field == "Password":
                left_entry.configure(show="*")
            left_entry.grid(row=row, column=1, padx=15, pady=12, sticky="w")
            self.entries[left_field] = left_entry

            right_label = ctk.CTkLabel(self.inner_frame, text=f"{right_field}:", font=("Arial", 16))
            right_label.grid(row=row, column=2, padx=15, pady=12, sticky="e")

            right_entry = ctk.CTkEntry(self.inner_frame, width=320, height=40, corner_radius=8)
            if right_field == "Password":
                right_entry.configure(show="*")
            right_entry.grid(row=row, column=3, padx=15, pady=12, sticky="w")
            self.entries[right_field] = right_entry

        # **Terms and Conditions Checkbox**
        self.accept_terms_var = ctk.BooleanVar()
        self.terms_checkbox = ctk.CTkCheckBox(
            self.inner_frame, text="I accept the Terms and Conditions",
            font=("Arial", 14), variable=self.accept_terms_var,
            command=self.toggle_register_button
        )
        self.terms_checkbox.grid(row=7, column=0, columnspan=4, pady=(10, 10))

        # Auto-generate Account Number
        self.generate_account_number()

        # Buttons Section
        button_frame = ctk.CTkFrame(self.outer_frame)
        button_frame.pack(pady=(0, 10))

        self.submit_button = ctk.CTkButton(
            button_frame, text="Register", fg_color="#007BFF", hover_color="#0056b3",
            text_color="white", width=130, height=40, command=self.save, state="disabled"
        )
        self.submit_button.grid(row=0, column=0, padx=20, pady=12)

        clear_button = ctk.CTkButton(button_frame, text="Clear", fg_color="#DC3545", hover_color="#A71D2A",
                                     text_color="white", width=130, height=40, command=self.clear)
        clear_button.grid(row=0, column=1, padx=20, pady=12)

    def toggle_register_button(self):
        if self.accept_terms_var.get():
            self.submit_button.configure(state="normal")
        else:
            self.submit_button.configure(state="disabled")

    def generate_account_number(self):
        con = sqlite3.connect('bank.db')
        cursor = con.cursor()
        cursor.execute("SELECT acno FROM cusdetails ORDER BY acno DESC LIMIT 1")
        last_acno = cursor.fetchone()
        new_acno = str(int(last_acno[0]) + 1).zfill(10) if last_acno else "1000000000"
        con.close()

        self.entries["Account Number"].configure(state="normal")
        self.entries["Account Number"].delete(0, "end")
        self.entries["Account Number"].insert(0, new_acno)
        self.entries["Account Number"].configure(state="disabled")

    def save(self):
        # Get field values
        bank_name = self.bank_dropdown.get().strip()
        ifsc_code = self.entries["IFSC Code"].get().strip()
        acno = self.entries["Account Number"].get()
        balance = self.entries["Balance"].get()
        name = self.entries["Name"].get().strip()
        contact = self.entries["Contact"].get().strip()
        address = self.entries["Address"].get().strip()
        aadhar = self.entries["Aadhar No"].get().strip()
        email = self.entries["E-Mail"].get().strip()
        pancard = self.entries["Pancard No"].get().strip()
        username = self.entries["User Name"].get().strip()
        password = self.entries["Password"].get().strip()

        # Check if any field is empty
        if (bank_name == "Select the Bank" or not ifsc_code or not name or not contact or not address or
                not aadhar or not email or not pancard or not username or not password):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Database connection
        con = sqlite3.connect('bank.db')
        cursor = con.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM cusdetails WHERE un=?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists. Choose another one.")
            con.close()
            return

        # Insert into database (with bank name & IFSC code added)
        try:
            cursor.execute("""
                INSERT INTO cusdetails (acno, nam, addr, con, mail, adhar, pan, un, pw, amt, bank, ifsc)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (
                           acno, name, address, contact, email, aadhar, pancard, username, password, balance, bank_name,
                           ifsc_code))

            con.commit()
            messagebox.showinfo("Success", "Customer Registered Successfully!")
            self.clear()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            con.close()

    def clear(self):
        self.bank_dropdown.set("Select the Bank")
        for key in self.entries:
            self.entries[key].configure(state="normal")
            self.entries[key].delete(0, "end")
            if key == "Balance":
                self.entries[key].insert(0, "1000.00")
                self.entries[key].configure(state="disabled")
            elif key == "Account Number":
                self.generate_account_number()
                self.entries[key].configure(state="disabled")

        self.accept_terms_var.set(False)
        self.submit_button.configure(state="disabled")

