import sqlite3

sac=sqlite3.connect('bank.db')

ath=sac.cursor()

ath.execute('drop table if exists cusdetails')

connec='''create table cusdetails(bank varchar(30),ifsc varchar(30),acno varchar(30),nam char(40),addr varchar(50),con varchar(10),mail varchar(40),adhar varchar(20),pan varchar(20),un varchar(20),pw varchar(20),amt int)'''

ath.execute(connec)

print("Table Craete Successfully")

sac.commit()

sac.close()
