import sqlite3
from datetime import datetime, timedelta

today = datetime.today().day # todays date it numerical value
start_of_week = today - datetime.now().date().weekday() # start of the week

with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT SUM(amount)
            FROM expense
            WHERE date BETWEEN ? AND ?""", (today, start_of_week)
        )

        total = cursor.fetchone()[0]

        if total is None:
            total = 0
            
        print(total)