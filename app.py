from flask import Flask, render_template, redirect, url_for,jsonify, request, session
import hashlib
from db_manager import *
import hashlib

app = Flask(__name__)

db_manager = DatabaseManager('pizzeria_rating.db')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        query = 'SELECT id FROM users WHERE username = ? AND password = ?'
        cursor = db_manager.execute_query(query, username, hashed_password)
        user = cursor.fetchone()
        
        if user:
            return redirect(url_for('index'))
        else:
            return "Invalid username or password", 403
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        query = 'INSERT INTO users (username, password) VALUES (?, ?)'
        try:
            db_manager.execute_query(query, username, hashed_password)
            return redirect(url_for('login'))
        except Exception as e:
            return f'Error: {e}'
    
    return render_template('register.html')

@app.route('/post_review', methods=['GET', 'POST'])
def post_review():
    if request.method == 'POST':
        pizzeria_id = request.form['pizzeria_id']
        review = request.form['review']
        rating = request.form['rating']
        user_id = 1

        query = 'INSERT INTO reviews (pizzeria_id, review, rating, predicted_by) VALUES (?, ?, ?, ?)'
        db_manager.execute_query(query, pizzeria_id, review, rating, user_id)
        return redirect(url_for('index'))

    query = 'SELECT id, name FROM pizzerias'
    pizzerias = db_manager.execute_query(query).fetchall()
    return render_template('post_review.html', pizzerias=pizzerias)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pizzerias', methods=['GET'])
def api_pizzerias():
    pizzerias = db_manager.execute_query('SELECT * FROM pizzerias').fetchall()
    return jsonify([dict(p) for p in pizzerias])

if __name__ == '__main__':
    app.run(debug=True)