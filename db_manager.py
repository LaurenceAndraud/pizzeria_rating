import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query, *args):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, args)
        self.conn.commit()
        return cursor

    def create_users(self):
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        '''
        self.execute_query(query)
    
    def create_pizzerias_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS pizzerias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                latitude TEXT,
                longitude TEXT,
                creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        '''
        self.execute_query(query)

    def create_reviews_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pizzeria_id INTEGER,
                review TEXT,
                rating INTEGER,
                review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pizzeria_id) REFERENCES pizzerias(id)
            );
        '''
        self.execute_query(query)

    def save_pizzeria(self, name, location, latitude, longitude):
        query = 'INSERT INTO pizzerias (name, location, latitude, longitude) VALUES (?, ?, ?, ?)'
        self.execute_query(query, name, location, latitude, longitude)

    def get_all_pizzerias(self):
        query = 'SELECT * FROM pizzerias'
        cursor = self.execute_query(query)
        return cursor.fetchall()
    
    def save_review(self, pizzeria_id, review, rating):
        query = 'INSERT INTO reviews (pizzeria_id, review, rating) VALUES (?, ?, ?)'
        self.execute_query(query, pizzeria_id, review, rating)

    def get_reviews_for_pizzeria(self, pizzeria_id):
        query = 'SELECT * FROM reviews WHERE pizzeria_id = ?'
        cursor = self.execute_query(query, pizzeria_id)
        return cursor.fetchall()
    
    def get_pizzeria_by_id(self, pizzeria_id):
        query = "SELECT * FROM pizzerias WHERE id = ?"
        cursor = self.execute_query(query, pizzeria_id)
        return cursor.fetchone()

    def get_user(self, username, hashed_password):
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        args = (username, hashed_password)
        cursor = self.execute_query(query, *args)
        user = cursor.fetchone()
        return user
        
    def save_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        self.execute_query(query, username, password)