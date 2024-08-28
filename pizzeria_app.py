from flask import Flask, request, jsonify
from db_manager import DatabaseManager

app = Flask(__name__)

class PizzeriaApp:
    def __init__(self, db_file):
        self.db = DatabaseManager(db_file)
        self.db.create_pizzerias_table()
        self.db.create_reviews_table()

        def add_pizzeria(self, name, location):
            self.db.save_pizzeria(name, location)

        def get_pizzeria(self):
            return self.db.get_all_pizzerias()
        
        def add_review(self, pizzeria_id, review, rating):
            self.db.save_review(pizzeria_id, review, rating)

        def get_review(self, pizzeria_id):
            return self.db.get_reviews_for_pizzeria(pizzeria_id)
        
pizzeria_app = PizzeriaApp('pizzeria_rating.db')

@app.route('/pizzerias', methods=['GET'])
def get_pizzerias():
    pizzerias = pizzeria_app.get_pizzerias()
    return jsonify(pizzerias)

@app.route('/pizzerias', methods=['POST'])
def add_pizzeria():
    data = request.json
    pizzeria_app.add_pizzeria(data['name'], data['address'], data.get('latitude'), data.get('longitude'))
    return jsonify({'status': 'Pizzeria added'}), 201

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    pizzeria_app.add_review(data['pizzeria_id'], data['review'], data['rating'])
    return jsonify({'status': 'Review added'}), 201

@app.route('/reviews/<int:pizzeria_id>', methods=['GET'])
def get_reviews(pizzeria_id):
    reviews = pizzeria_app.get_reviews(pizzeria_id)
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(debug=True)