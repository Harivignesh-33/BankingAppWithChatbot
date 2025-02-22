import sqlite3

ar=sqlite3.connect("bank.db")

js=ar.cursor()

js.execute('''select * from cusdetails''')

result=js.fetchone()

print(result)

result=js.fetchall()

print(result)

ar.commit()

ar.close()
