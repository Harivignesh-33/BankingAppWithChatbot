from tkinter import *
from tkinter import messagebox

# Create main window
bank = Tk()
bank.geometry("400x450")
bank.title("Login Form")
bank.config(bg="#f4f4f4")

# Frame for Login
frame = Frame(bank, bg="#ffffff", padx=20, pady=20, relief=RAISED, bd=2)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Title Label
Label(frame, text="Customer Login", bg="#ffffff", fg="#333333", font=("Arial", 18, "bold")).pack(pady=10)

# Username
Label(frame, text="Username", bg="#ffffff", fg="#555555", font=("Arial", 12)).pack(anchor=W)
un = Entry(frame, width=30, font=("Arial", 12), bd=2, relief=GROOVE)
un.pack(pady=5)

# Password
Label(frame, text="Password", bg="#ffffff", fg="#555555", font=("Arial", 12)).pack(anchor=W)
pw = Entry(frame, width=30, font=("Arial", 12), bd=2, relief=GROOVE, show="*")
pw.pack(pady=5)

# Buttons
btn_frame = Frame(frame, bg="#ffffff")
btn_frame.pack(pady=15)

Button(btn_frame, text="Login", width=10, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), bd=0, relief=FLAT).pack(side=LEFT, padx=5)
Button(btn_frame, text="Cancel", width=10, bg="#FF5733", fg="white", font=("Arial", 12, "bold"), bd=0, relief=FLAT, command=bank.quit).pack(side=LEFT, padx=5)

# Run application
bank.mainloop()
