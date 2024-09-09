from flask import Flask, render_template, request, redirect, url_for, make_response
import hashlib
from db_manager import DatabaseManager

app = Flask(__name__)

def get_db_manager():
    return DatabaseManager('pizzeria_rating.db')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        db_manager = get_db_manager()
        user = db_manager.get_user(username, hashed_password)

        if user:
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('user_id', str(user[0]))
            resp.set_cookie('username', user[1])
            return resp
        else:
            return "Invalid credentials, please try again."
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('user_id', '', expires=0)
    resp.set_cookie('username', '', expires=0)
    return resp

@app.route('/add_pizzeria', methods=['GET', 'POST'])
def add_pizzeria():
    if not request.cookies.get('user_id'):
        return "You need to be logged in to add a pizzeria."

    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        db_manager = get_db_manager()
        db_manager.save_pizzeria(name, location, latitude, longitude)
        
        return redirect(url_for('index'))

    return render_template('add_pizzeria.html')

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    user_id = request.cookies.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        pizzeria_id = request.form['pizzeria_id']
        review = request.form['review']
        rating = int(request.form['rating'])

        db_manager = get_db_manager()
        db_manager.save_review(pizzeria_id, review, rating)

        return redirect(url_for('index'))

    pizzeria_id = request.args.get('pizzeria_id')
    if pizzeria_id:
        db_manager = get_db_manager()
        pizzeria = db_manager.get_pizzeria_by_id(pizzeria_id)
        return render_template('add_review.html', pizzeria=pizzeria)
    
    return "Pizzeria ID is required."

@app.route('/')
def index():
    user_id = request.cookies.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    db_manager = get_db_manager()
    pizzerias = db_manager.get_all_pizzerias()
    username = request.cookies.get('username')

    return render_template('index.html', pizzerias=pizzerias, user=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        db_manager = get_db_manager()
        if db_manager.get_user(username, hashed_password):
            return "Username already exists."
        db_manager.save_user(username, hashed_password)
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

