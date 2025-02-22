import sqlite3
import customtkinter as ctk
from tkinter import messagebox, simpledialog
import sys
import csv
import os
from fpdf import FPDF
from tkinter import filedialog

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class BankingChatBotGUI:
    def __init__(self, root, account_no, customer_name):
        self.root = root
        self.root.title("Banking ChatBot")
        self.root.attributes('-fullscreen', True)  # Open in full-screen mode
        self.conn = sqlite3.connect('bank.db')
        self.cursor = self.conn.cursor()
        self.account_no = account_no
        self.customer_name = customer_name

        if not self.validate_account():
            messagebox.showerror("Error", "Invalid account number! Exiting chatbot.")
            self.root.destroy()
            return

        self.chatbot_responses = {
            "what is my balance?": self.get_balance,
            "balance?": self.get_balance,
            "balance": self.get_balance,
            "bal": self.get_balance,
            "show my last transaction": self.get_last_transaction,
            "how many transactions have i made?": self.get_transaction_count,
        }

        self.create_ui()

    def validate_account(self):
        self.cursor.execute('SELECT acno FROM cusdetails WHERE acno = ?', (self.account_no,))
        return bool(self.cursor.fetchone())

    def create_ui(self):
        self.frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.frame.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.9)

        self.label = ctk.CTkLabel(self.frame, text=f"Hello, {self.customer_name}!", font=("Arial", 18, "bold"))
        self.label.pack(pady=10)

        self.chat_display = ctk.CTkTextbox(self.frame, height=400, width=800, state='disabled', font=("Arial", 19))
        self.chat_display.pack(pady=15, fill='both', expand=True)

        entry_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        entry_frame.pack(pady=10, fill="both", expand=True)

        self.chat_entry = ctk.CTkEntry(entry_frame, font=("Arial", 14))
        self.chat_entry.pack(side='left', padx=10, pady=10, fill='both', expand=True)

        self.ask_button = ctk.CTkButton(entry_frame, text="Send", command=self.get_chatbot_response, fg_color="#1E90FF", hover_color="#1C86EE")
        self.ask_button.pack(side='right', padx=10)

        self.sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=15)
        self.sidebar.place(relx=0.02, rely=0.05, relwidth=0.2, relheight=0.9)

        button_names = [
            ("Show Balance", self.show_balance),
            ("View Transactions", self.view_transactions),
            ("Transactions in Range", self.view_transactions_range),
            ("Exit", self.exit_app)
        ]

        for text, command in button_names:
            btn = ctk.CTkButton(self.sidebar, text=text, command=command, fg_color="#1E90FF", hover_color="#1C86EE")
            btn.pack(pady=10, fill='x')

    def get_balance(self):
        self.cursor.execute('SELECT amt FROM cusdetails WHERE acno = ?', (self.account_no,))
        balance = self.cursor.fetchone()
        return f"Your current balance is: ₹{balance[0]:.2f}" if balance else "Account not found!"

    def get_last_transaction(self):
        self.cursor.execute("SELECT tt, amt, dat FROM trans WHERE acno = ? ORDER BY dat DESC LIMIT 1",
                            (self.account_no,))
        transaction = self.cursor.fetchone()

        if transaction:
            try:
                amount = float(transaction[1])  # Ensure the amount is a float
                return f"Last transaction: {transaction[0]} of ₹{amount:.2f} on {transaction[2]}"
            except (ValueError, TypeError):
                return "Error: Invalid transaction data."

        return "No transactions found."

    def get_transaction_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM trans WHERE acno = ?", (self.account_no,))
        count = self.cursor.fetchone()
        return f"You have made {count[0]} transactions." if count else "No transactions found."

    def get_chatbot_response(self):
        question = self.chat_entry.get().strip().lower()
        if not question:
            return

        answer = self.chatbot_responses.get(question, lambda: "I'm sorry, I don't have an answer to that question.")()

        self.chat_display.configure(state='normal')

        # Add spacing and formatting for better readability
        self.chat_display.insert('end', "\n", 'left_align')  # Add a newline for separation
        self.chat_display.insert('end', f"You: {question}\n", 'right_align')
        self.chat_display.insert('end', f"Bot: {answer}\n\n", 'left_align')

        self.chat_display.configure(state='disabled')
        self.chat_entry.delete(0, 'end')


    def show_balance(self):
        self.show_alert("Balance", self.get_balance())

    def view_transactions(self):
        self.cursor.execute("SELECT tt, amt, dat FROM trans WHERE acno = ? ORDER BY dat DESC", (self.account_no,))
        transactions = self.cursor.fetchall()

        if not transactions:
            self.show_alert("Transactions", "No transactions found.")
            return

        trans_text = "Transaction Type | Amount | Date\n" + "-" * 40 + "\n"
        for trans in transactions:
            trans_text += f"{trans[0]} | ₹{float(trans[1]):.2f} | {trans[2]}\n"

        self.show_alert("Transactions", trans_text)

    def show_alert(self, title, message):
        top = ctk.CTkToplevel(self.root)
        top.title(title)
        top.geometry("400x300")
        top.grab_set()  # Ensures focus remains on this window
        label = ctk.CTkLabel(top, text=message, wraplength=380, font=("Arial", 12))
        label.pack(pady=20)
        close_button = ctk.CTkButton(top, text="OK", command=top.destroy)
        close_button.pack(pady=10)

    def view_transactions_range(self):
        start_date = simpledialog.askstring("Transaction Range", "Enter start date (YYYY-MM-DD):", parent=self.root)
        if not start_date:
            return

        end_date = simpledialog.askstring("Transaction Range", "Enter end date (YYYY-MM-DD):", parent=self.root)
        if not end_date:
            return

        self.cursor.execute(
            "SELECT tt, amt, dat FROM trans WHERE acno = ? AND dat BETWEEN ? AND ? ORDER BY dat DESC",
            (self.account_no, start_date, end_date)
        )
        transactions = self.cursor.fetchall()

        if not transactions:
            messagebox.showinfo("Transactions", "No transactions found in the given range.", parent=self.root)
            return

        trans_text = "Transaction Type | Amount | Date\n" + "-" * 40 + "\n"
        for trans in transactions:
            trans_text += f"{trans[0]} | ₹{float(trans[1]):.2f} | {trans[2]}\n"

        messagebox.showinfo("Transactions", trans_text, parent=self.root)

        export_choice = messagebox.askyesno("Export", "Would you like to export these transactions?", parent=self.root)
        if export_choice:
            export_format = messagebox.askquestion("Export Format", "Export as CSV or PDF? (yes for CSV, no for PDF)",
                                                   parent=self.root)
            if export_format == 'yes':
                self.export_transactions_csv(transactions)
            else:
                self.export_transactions_pdf(transactions)

    def export_transactions_pdf(self, transactions):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF Files", "*.pdf")],
                                                 title="Save PDF File")

        if not file_path:
            return  # User canceled the save dialog

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Add a Unicode font that supports ₹ symbol
        font_path = r"C:\Users\Admin\AppData\Local\Microsoft\Windows\Fonts\DejaVuSans-Bold.ttf"
        if os.path.exists(font_path):
            pdf.add_font("ArialUnicode", "", font_path, uni=True)
            pdf.set_font("ArialUnicode", "", 12)
        else:
            messagebox.showwarning("Font Warning", "Unicode font not found! Using default font.")
            pdf.set_font("Helvetica", "", 12)  # Fallback

        pdf.cell(200, 10, f"Transaction Report - {self.customer_name}", ln=True, align='C')
        pdf.ln(10)

        pdf.cell(60, 10, "Transaction Type", border=1)
        pdf.cell(50, 10, "Amount", border=1)
        pdf.cell(50, 10, "Date", border=1)
        pdf.ln()

        for trans in transactions:
            pdf.cell(60, 10, trans[0], border=1)
            pdf.cell(50, 10, f"₹{float(trans[1]):.2f}", border=1)
            pdf.cell(50, 10, trans[2], border=1)
            pdf.ln()

        pdf.output(file_path, "F")
        messagebox.showinfo("Export Successful", f"Transactions exported successfully as {file_path}.")

    def export_transactions_csv(self, transactions):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv")],
                                                 title="Save CSV File")

        if not file_path:
            return  # User canceled the save dialog

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Transaction Type", "Amount", "Date"])
            writer.writerows(transactions)

        messagebox.showinfo("Export Successful", f"Transactions exported successfully as {file_path}.")

    def exit_app(self):
        self.conn.close()
        self.root.quit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Missing login details! Open chatbot from Homepage.")
        sys.exit()

    account_no = sys.argv[1]
    customer_name = sys.argv[2]
    root = ctk.CTk()
    app = BankingChatBotGUI(root, account_no, customer_name)
    root.mainloop()
