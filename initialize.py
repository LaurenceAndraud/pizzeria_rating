from db_manager import DatabaseManager

def initialize_database():
    db = DatabaseManager('pizzeria_rating.db')
    db.create_pizzerias_table()
    db.create_reviews_table()

if __name__ == '__main__':
    initialize_database()