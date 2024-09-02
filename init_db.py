from db_manager import *

def intialize_database():
    db_manager = DatabaseManager('pizzeria_rating.db')
    db_manager.create_users()
    db_manager.create_pizzerias_table()
    db_manager.create_reviews_table()
    db_manager.close()

if __name__ == "__main__":
    intialize_database()
    print("Database initialized successfully")