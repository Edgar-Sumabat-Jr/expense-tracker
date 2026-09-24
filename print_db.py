import sqlite3

conn = sqlite3.connect("storage.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM expense")

for row in cursor:
    print(row)

conn.close()