import sqlite3
import subprocess  # ✅ To open chatbot.py with credentials
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

import adminpage
import customerpage


class CustomEntry(ctk.CTkFrame):
    def __init__(self, parent, placeholder, is_password=False):
        super().__init__(parent, fg_color="transparent")
        self.is_password = is_password
        self.show_password = False
        self.entry = ctk.CTkEntry(self, width=350, height=40, placeholder_text=placeholder, show="*" if is_password else "")
        self.entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        if is_password:
            self.eye_button = ctk.CTkButton(self, text="👁", width=30, height=30,
                                            fg_color="transparent", text_color="#666",
                                            hover_color="#DDD", command=self.toggle_password)
            self.eye_button.place(relx=0.92, rely=0.5, anchor='center')

    def toggle_password(self):
        self.show_password = not self.show_password
        self.entry.configure(show="" if self.show_password else "*")

    def get(self):
        return self.entry.get()

    def delete(self, start, end):
        self.entry.delete(start, end)

class Homepage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart Banking - Login")
        self.state("zoomed")
        self.after(100, lambda: self.state("zoomed"))
        self.configure(bg="#F8F9FA")

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(padx=50, pady=50, fill='both', expand=True)

        form_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", width=450, height=500, corner_radius=15)
        form_frame.pack(side='left', padx=50, pady=50, fill='both', expand=True)

        title_label = ctk.CTkLabel(form_frame, text="Welcome to Smart Banking",
                                   font=("Arial", 26, "bold"), text_color="#333333")
        title_label.pack(anchor='center', pady=(20, 5))

        subtitle_label = ctk.CTkLabel(form_frame, text="Login to continue",
                                      font=("Arial", 16), text_color="#666666")
        subtitle_label.pack(anchor='center', pady=(30, 0))

        self.username_entry = CustomEntry(form_frame, "Username")
        self.username_entry.pack(pady=20)

        self.password_entry = CustomEntry(form_frame, "Password", is_password=True)
        self.password_entry.pack(pady=20)

        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        login_button = ctk.CTkButton(button_frame, text="Login", font=("Arial", 18, "bold"),
                                     width=160, height=50, fg_color="#2ECC71", hover_color="#27AE60",
                                     command=self.login)
        login_button.grid(row=0, column=0, padx=10)

        self.chatbot_button = ctk.CTkButton(button_frame, text="Login to Chatbot", font=("Arial", 18, "bold"),
                                            width=160, height=50, fg_color="#3498DB", hover_color="#2980B9",
                                            command=self.open_chatbot)
        self.chatbot_button.grid(row=0, column=1, padx=10)

        register_label = ctk.CTkLabel(form_frame, text="New to the application? First register yourself",
                                      font=("Arial", 14), text_color="#666666")
        register_label.pack(pady=(10, 5))

        customer_button = ctk.CTkButton(form_frame, text="New Registration", font=("Arial", 18, "bold"),
                                        width=350, height=50, fg_color="#E74C3C", hover_color="#C0392B",
                                        command=self.customer_details)
        customer_button.pack(pady=10)

        illustration_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=15, width=600, height=500)
        illustration_frame.pack(side='right', padx=0, pady=0, fill='both', expand=True)
        illustration_frame.pack_propagate(False)

        self.image_path = "./Images/home_img.jpg"
        self.illustration_image = ctk.CTkImage(light_image=Image.open(self.image_path),
                                               dark_image=Image.open(self.image_path),
                                               size=(580, 480))
        self.illustration_label = ctk.CTkLabel(illustration_frame, image=self.illustration_image, text="",
                                               fg_color="#FFFFFF", corner_radius=15)
        self.illustration_label.pack(padx=10, pady=10, expand=True)

        self.user_info = None  # ✅ Store logged-in user info

    def login(self):
        """Handles user login authentication."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showinfo("Alert", "Please enter Username & Password")
            return

        if username == "admin" and password == "admin":
            self.destroy()
            admin_window = adminpage.AdminPage()
            admin_window.mainloop()
            return

        try:
            with sqlite3.connect("bank.db") as con:
                csr = con.cursor()
                csr.execute("SELECT acno, nam FROM cusdetails WHERE un=? AND pw=?", (username, password))
                res = csr.fetchone()

            if not res:
                messagebox.showinfo("Message", "Invalid User or First register your details")
            else:
                acc_no, customer_name = res  # ✅ Corrected variable assignment
                self.user_info = (username, password, acc_no)

                self.withdraw()
                customer_window = customerpage.CustomerPage(self, acc_no, customer_name)
                customer_window.state("zoomed")
                customer_window.focus_force()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def open_chatbot(self):
        """Fetches account number using username & password, then opens chatbot."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter your Username & Password to access the chatbot.")
            return

        try:
            with sqlite3.connect("bank.db") as con:
                csr = con.cursor()
                csr.execute("SELECT acno, nam FROM cusdetails WHERE un=? AND pw=?", (username, password))
                res = csr.fetchone()

            if not res:
                messagebox.showerror("Error", "Invalid Username or Password! Please try again.")
                return

            acc_no, customer_name = res  # ✅ Extract account number and name

            # ✅ Open chatbot with fetched account number and customer name
            subprocess.Popen(["python", "chatbot.py", str(acc_no), customer_name])

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def customer_details(self):
        """Opens customer registration page."""
        self.iconify()
        from customerdetailshome import CustomerRegistration
        user_window = ctk.CTkToplevel(self)
        user_window.geometry("800x650")
        user_window.title("Customer Registration")
        CustomerRegistration(user_window)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = Homepage()
    app.run()
