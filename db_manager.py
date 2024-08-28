import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)

    def close(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, *args):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, args)
        self.conn.commit()
        return cursor
    
    def create_pizzerias_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS pizzerias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
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

    def save_pizzeria(self, name, location):
        query = 'INSERT INTO pizzerias (name, location) VALUES (?, ?)'
        self.execute_query(query, name, location)

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