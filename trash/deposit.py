from tkinter import *
from tkinter import messagebox,ttk
import sqlite3
bank=Tk()

bank.geometry("550x450")

bank.title("Transaction Form")

bank.config(bg="#C1C8E4")



lab=Label(bank,text="Transaction",bg="#C1C8E4",fg="#116466",font=("Times New Roman",22,"bold")).place(x=160,y=60)

lab1=Label(bank,text="Account Number",bg="#C1C8E4",fg="#2C2E39",font=("Times New Roman",18,"bold")).place(x=20,y=140)
an=Entry(bank,width=30)
an.place(x=280,y=145)


lab2=Label(bank,text="Deposit Amount",bg="#C1C8E4",fg="#2C2E39",font=("Times New Roman",18,"bold")).place(x=20,y=190)
da=Entry(bank,width=30)
da.place(x=280,y=195)


Button(bank,text="Submit",width=20,bg="#FFCB9A",font=("Times New Roman",12,"bold"),fg="#2C3531").place(x=30,y=300)
Button(bank,text="View Balance",width=20,bg="#FFCB9A",font=("Times New Roman",12,"bold"),fg="#2C3531").place(x=300,y=300)

bank.mainloop()
