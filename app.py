from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM kpis ORDER BY week ASC').fetchall()
    conn.close()
    
    weeks = [row['week'] for row in data]
    revenue = [row['revenue'] for row in data]
    expenses = [row['expenses'] for row in data]
    profit = [row['profit'] for row in data]
    
    return render_template('dashboard.html', weeks=weeks, revenue=revenue,
                           profit = profit, expenses = expenses)

@app.route('/add', methods=['POST'])
def add_data():
    week = request.form['week']
    revenue = float(request.form['revenue'])
    expenses = float(request.form['expenses'])
    profit = revenue - expenses
    
    conn = get_db_connection()
    conn.execute('INSERT INTO kpis (week, revenue, expenses, profit) VALUES(?, ?, ?, ?)',
                 (week, revenue, expenses, profit))
    conn.commit()
    conn.close()
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
    