import sqlite3

database = "expenses.db"
create_table = (""" CREATE TABLE IF NOT EXISTS expense (
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT,
                    description TEXT
                        )""")

create_common_expenses_table = (""" CREATE TABLE IF NOT EXISTS common_expense (
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT
                        )""")

with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    cursor.execute(create_table)
    cursor.execute(create_common_expenses_table)
    conn.commit()

    cursor.close()