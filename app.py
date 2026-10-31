from flask import Flask, render_template, request, redirect, jsonify, make_response
import sqlite3
from datetime import datetime, date
import logging


today = datetime.now().date()

app = Flask(__name__)

import sqlite3
from flask import g

DATABASE = 'expenses.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def show_table():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT name, amount, date, description FROM expense")
    items = cursor.fetchall()


    cursor.execute("SELECT name, amount, date FROM common_expense")
    common_expenses = cursor.fetchall()

    return render_template(
            # table for expenses
            "home.html", 
            items=items,
            datetime=datetime,
            
            # common expenses
            common_expenses=common_expenses
        )


def insert_expense(name, amount, date, description):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("INSERT INTO expense (name, amount, date, description) VALUES (?, ?, ?, ?)",
                    (name, amount, date.isoformat(), description))

    db.commit()


@app.route("/add", methods=["POST"])
def add_expense():
    date = request.form.get("date", "").strip()
    amount = request.form.get("amount")
    description = request.form.get("description")


    response_text = (
    "Invalid date: Use MM-DD-YYYY Example: 10-27-2026\n"
    "or just leave it blank to use the date today"
)

    if date == "":
        date = today
    else:
        try:
            date = datetime.strptime(date, "%m-%d-%Y").date()
        except ValueError:
            return make_response(response_text, 400, {"Content-Type": "text/plain"})


    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return "use whole number only", 400
    
    if amount <= 0:
        return "Amount must be greater than 0", 400

    if description == '':
        description = "normal expense"


    insert_expense(
        request.form.get("expense-name"),
        amount,
        date,
        description
    )
    return redirect("/")


@app.route("/total-expenses")
def total_expenses():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT SUM(amount) FROM expense")

    result = cursor.fetchone()

    total_sum = result[0] if result[0] is not None else 0.0

    return jsonify({"total": total_sum})


from datetime import datetime, timedelta
@app.route("/expenses/weekly")
def weekly_expenses():
    start_of_week = today - timedelta(days=today.weekday())

    db = get_db()
    cursor = db.cursor()
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

    db = get_db()
    cursor = db.cursor()
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


@app.route("/expenses/yearly")
def yearly_expense():
    year = date.today().year
    month = date.today().month

    start_of_year = date(year, 1, 1).isoformat()
    end_of_year = date(year, 12, 31).isoformat()

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT SUM(amount)
        FROM expense
        WHERE date BETWEEN ? AND ?
        """, (start_of_year, end_of_year)
        )

    total = cursor.fetchone()[0]

    if total is None:
        total = 0.0

    return jsonify({
        "start_of_year":start_of_year,
        "end_of_year":end_of_year,
        "total":total
    })


@app.route("/insert-common", methods=["POST"])
def insert_common_expense():
    json_data = request.get_json()

    name = json_data.get("name")
    amount = json_data.get("amount")
    today = datetime.now().date()

    if not name or amount is None or str(amount).strip() == "":
        return {"error": "backend server: name and amount required"}, 400
    
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute("INSERT INTO common_expense (name, amount, date) VALUES (?, ?, ?)",
                    (name, amount, today.isoformat()))

    db.commit()
    return {"success":"True"}, 201


@app.route("/add-common", methods=["POST"])
def add_common_expense():
    name = request.form.get("common-expense") # gets the inputs by the user from the frontend html form

    db = get_db()
    cursor = db.cursor()

    # finds the name of the common expense
    cursor.execute("SELECT name, amount FROM common_expense WHERE name = ?",
                   (name,))

    expense = cursor.fetchone()

    if expense is None:
        return "Common expense not found", 404

    today = datetime.now().date()
    
    insert_expense(
        expense[0],
        expense[1],
        today,
        "common expense"
    )

    return redirect("/")