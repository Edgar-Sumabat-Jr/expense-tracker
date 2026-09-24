from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime, date

today = datetime.now().date()

app = Flask(__name__)

@app.route("/")
def show_table():
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT name, amount, date, description FROM expense")
        items = cursor.fetchall()
        print(len(items))

    return render_template("home.html", items=items)


def insert_expense(name, amount, date, description):
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO expense (name, amount, date, description) VALUES (?, ?, ?, ?)",
                       (name, amount, date.isoformat(), description))

        conn.commit()


@app.route("/add", methods=["POST"])
def add_expense():
    date = request.form["date"]
    if date == '':
        date = today
    else:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    
    insert_expense(
        request.form["expense-name"],
        float(request.form["amount"]),
        date,
        request.form["description"]
    )
    return redirect("/")


@app.route("/add-common", methods=["POST"])
def common_expense():
    amount = float(request.form["common-expense"]) # we used the value="20" at the html frontend

    insert_expense(
        "pamasahe",
        amount,
        today,
        "pamasahe to"
    )

    return redirect("/")

@app.route("/total-expenses")
def total_expenses():
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expense")

        result = cursor.fetchone()

        total_sum = result[0] if result[0] is not None else 0.0

    return jsonify({"total": total_sum})

from datetime import datetime, timedelta
@app.route("/expenses/weekly")
def weekly_expenses():
    start_of_week = today - timedelta(days=today.weekday())

    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT SUM(amount)
            FROM expense
            WHERE date BETWEEN ? AND ?
            """, (start_of_week, today)
        )

        total = cursor.fetchone()[0]

        if total is None:
            total = 0.0

    return jsonify({
        "today":today,
        "start_of_week":start_of_week,
        "total":total
    })

import calendar
@app.route("/expenses/monthly")
def monthly_expenses():
    year = date.today().year
    month = date.today().month

    # calendar.monthrange returns array containing
    # weekday and day [weekday, day] we use [1] to access the day
    last_day = calendar.monthrange(year, month)[1] 
    start_of_month = date(year, month, 1).isoformat()
    end_of_month = date(year, month, last_day).isoformat()

    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """                                      
            SELECT SUM(amount)
            FROM expense
            WHERE date BETWEEN ? AND ?
            """, (start_of_month, end_of_month)
            )
        total = cursor.fetchone()[0]

        if total is None:
            total = 0.0

    return jsonify({
        "start_date":start_of_month,
        "end_date":end_of_month,
        "total":total
    })