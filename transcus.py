from tkinter import ttk
import tkinter as tk
import sqlite3


# ethukunee thrla intha moduleee




class trans:
    def __init__(self,root):
        self.root=root
        self.tree=ttk.Treeview(self.root,column=("c1","c2","c3","c4","c5"),show='headings')

        self.tree.column("#1",anchor=tk.CENTER)
        self.tree.heading("#1",text='Account Number')
        self.tree.column("#2",anchor=tk.CENTER)
        self.tree.heading("#2",text='Name')
        self.tree.column("#3",anchor=tk.CENTER)
        self.tree.heading("#3",text='Date')
        self.tree.column("#4",anchor=tk.CENTER)
        self.tree.heading("#4",text='Transaction Type')
        self.tree.column("#5",anchor=tk.CENTER)
        self.tree.heading("#5",text='Transaction Amount')
        self.tree.pack()

        a=tk.Button(self.root,text="Display Data",command=self.view)
        a.pack(pady=6)

    def view(self):
        self.con=sqlite3.connect('bank.db')
        self.csr=self.con.cursor()
        self.csr.execute("select * from trans")
        self.rows=self.csr.fetchall()

        for i in self.rows:
            self.tree.insert("",tk.END,values=i)
            self.con.close()
        
        
    
