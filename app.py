import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# Import your database configuration
from config import DATABASE_CONFIG

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# --- CORRECTED DATABASE CONNECTION ---
# Construct the database URI from your imported config file.
# This makes your app connect to your Cloud SQL database.
app.config['SQLALCHEMY_DATABASE_URI'] = (
f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- NO CHANGES BELOW THIS LINE ---
# Your database model and application logic remain exactly the same.

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    notes = db.Column(db.String(512), nullable=True)

@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_spent = sum(e.amount for e in expenses)
    # Note: You may want to update the hardcoded "2025-08" to be dynamic in the future
    this_month = sum(e.amount for e in expenses if e.date.startswith("2025-08"))
    categories = {}
    for e in expenses:
        categories[e.category] = categories.get(e.category, 0) + e.amount
    biggest_category = "-"
    if categories:
        cat, val = max(categories.items(), key=lambda x: x[1])
        biggest_category = f"{cat} (₹{val:.2f})"

    labels = list(categories.keys())
    data = list(categories.values())

    return render_template(
        "index.html",
        expenses=expenses,
        total_spent=f"₹{total_spent:,.2f}",
        this_month=f"₹{this_month:,.2f}",
        biggest_category=biggest_category,
        labels=labels,
        data=data,
        theme='theme-light'
    )

@app.route("/add", methods=["POST"])
def add():
    data = request.form
    expense = Expense(
        date=data["date"],
        description=data["description"],
        amount=float(data["amount"]),
        category=data["category"],
        notes=data.get("notes", "")
    )
    db.session.add(expense)
    db.session.commit()
    flash('Expense added!')
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    expense = Expense.query.get_or_404(id)
    if request.method == "POST":
        
        expense.date = request.form["date"]
        expense.description = request.form["description"]
        expense.amount = float(request.form["amount"])
        expense.category = request.form["category"]
        expense.notes = request.form.get("notes", "")
        db.session.commit()
        flash("Expense updated!")
        return redirect(url_for("index"))
    return render_template("edit.html", expense=expense, theme='theme-light')

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted!")
    return redirect(url_for("index"))
if __name__ == "__main__":
    with app.app_context():
        # This will create the 'expense' table based on your model if it doesn't exist
        db.create_all()
    # Run on 0.0.0.0 to be accessible from outside the container/VM
    # Use a port like 5000 for Gunicorn and Nginx to connect to
    app.run(host='0.0.0.0', port=5000, debug=True)
