from logging import exception
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"
    

@app.route('/')
def intex():
    return 'Hello!'

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}

        output.append(drink_data)
    return {"drinks": output}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}

@app.route('/drinks', methods=['POST']) # own POST expression to add a drink (add json value on PostMan)
# { "name": "Cola", "description": "delicious" }
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "successfully deleted!"}

## PUT method! (not part of the video)

@app.route('/drinks/<id>', methods=['PUT'])
def modify_drink(id):
    drink = Drink.query.get(id)
    if not drink:
        return {"message": "Drink not found!"} ## may not need jsonify(...)
    
    if 'name' in request.json:
        drink.name = request.json['name']
    if 'description' in request.json:
        drink.description = request.json['description']

    ## try and catch here: return jsonify({"message": "Drink updated successfully"}, 200) || jsonify({"message": "unable to update drink"}, 404) 
        db.session.commit()

