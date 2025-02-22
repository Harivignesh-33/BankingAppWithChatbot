import sqlite3

sac=sqlite3.connect('bank.db')

ath=sac.cursor()

ath.execute('drop table if exists trans')

connec='''create table trans(acno varchar(30),nam char(40),dat varchar(20),tt varchar(40),amt varchar(15))'''

ath.execute(connec)

print("Table Craete Successfully")

sac.commit()

sac.close()
