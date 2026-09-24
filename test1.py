import sqlite3

database = "storage.db"
create_table = (""" CREATE TABLE IF NOT EXISTS expense (
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT,
                    description TEXT
                        )""")

expense = ("pamasahe", 20, "2026-09-4", "pauwe")
add_rows = """ INSERT INTO expense (name, amount, date, description) 
                VALUES (?, ?, ?, ?) """
            

with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    cursor.execute(create_table)
    cursor.execute(add_rows, expense)
    conn.commit()

