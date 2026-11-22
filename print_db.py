import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM expense") # change to common_expense to print the common expenses if needed

for row in cursor:
    print(row)

conn.close()