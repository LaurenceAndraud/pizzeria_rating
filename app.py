from flask import Flask, render_template, redirect, url_for,jsonify, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from db_manager import *
import hashlib

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

db_manager = DatabaseManager('pizzeria_rating.db')

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    query = "SELECT id, username FROM users WHERE id = ?"
    cursor = db_manager.execute_query(query, user_id)
    user = cursor.fetchone()
    if user :
        return User(user[0], user[1])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexigest()

        query = 'SELECT id FROM users WHERE username = ? AND password = ?'
        cursor = db_manager.execute_query(query, username, hashed_password)
        user = cursor.fetchone()
        
        if user:
            user_obj = User(user[0], username)
            login_user(user_obj)
            return redirect(url_for('index'))
        return 'Invalid credentials'
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
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
@login_required
def post_review():
    if request.method == 'POST':
        pizzeria_id = request.form['pizzeria_id']
        review = request.form['review']
        rating = request.form['rating']
        user_id = current_user.id

        query = 'INSERT INTO reviews (pizzeria_id, review, rating, predicted_by) VALUES (?, ?, ?, ?)'
        db_manager.execute_query(query, pizzeria_id, review, rating, user_id)
        return redirect(url_for('index'))

    query = 'SELECT id, name FROM pizzerias'
    pizzerias = db_manager.execute_query(query).fetchall()
    return render_template('post_review.html', pizzerias=pizzerias)

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/api/pizzerias', methods=['GET'])
def api_pizzerias():
    pizzerias = db_manager.execute_query('SELECT * FROM pizzerias').fetchall()
    return jsonify([dict(p) for p in pizzerias])

if __name__ == '__main__':
    app.run(debug=True)