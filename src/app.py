"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planetas, Personajes, Vehiculos, Favorito
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

"""--------------------------_<User>_--------------------------------"""

@app.route('/user', methods=['GET'])
def handle_hello():
    all_users = User.query.all()  # Consulta todos los usuarios de la base de datos
    user_list = list(map(lambda user: user.serialize(), all_users))  #  cada objeto User usando lambda

    if not user_list:
        return jsonify({'msj': 'no hay usuarios'}), 404  # Devuelve una respuesta

    return jsonify(user_list), 200  # Devuelve la lista de usuarios  



"""--------------------------_<Personajes>_--------------------------------"""

# Ruta para obtener personajes
@app.route('/personajes', methods=['GET'])
def handle_personajes():
    todos_personajes = Personajes.query.all()
    lista_personajes = list(map(lambda personaje: personaje.serialize(), todos_personajes))

    return jsonify(lista_personajes), 200


# Ruta para obtener un personaje por su ID

@app.route('/personajes/<int:personajes_id>', methods=['GET'])
def handle_personajes_id(personajes_id):
    personaje = Personajes.query.get(personajes_id)

    if personaje is None:
        return jsonify({"mensaje": "Personaje no encontrado"}), 404

    return jsonify(personaje.serialize()), 200

# Crear un nuevo personaje

@app.route('/personajes', methods=['POST'])
def create_personaje():
    request_body = json.loads(request.data)
    existing_personaje = Personajes.query.filter_by(**request_body).first()

    if existing_personaje:
        return jsonify({"message": "El personaje ya existe"}), 400

    new_personaje = Personajes(**request_body)
    db.session.add(new_personaje)
    db.session.commit()
    
    return jsonify(new_personaje.serialize()), 200


"""--------------------------_<Planetas>_--------------------------------"""
# Ruta para obtener planeta

@app.route('/planetas', methods=['GET'])
def handle_planetas():
    todos_planetas = Planetas.query.all()
    lista_planetas = list(map(lambda planeta: planeta.serialize(), todos_planetas))

    return jsonify(lista_planetas), 200

# Ruta para obtener un planeta por su ID

@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def handle_planetas_id(planetas_id):
    planeta = Planetas.query.get(planetas_id)

    if planeta is None:
        return jsonify({"mensaje": "Planeta no encontrado"}), 404

    return jsonify(planeta.serialize()), 200

"""--------------------------_<Vehiculos>_--------------------------------"""

# Ruta para obtener vehiculos

@app.route('/vehiculos', methods=['GET'])
def handle_vehiculos():
    todos_vehiculos = Vehiculos.query.all()
    lista_vehiculos = list(map(lambda vehiculo: vehiculo.serialize(), todos_vehiculos))

    return jsonify(lista_vehiculos), 200

# Ruta para obtener un vehículo por su ID

@app.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def handle_vehiculo_id(vehiculo_id):
    vehiculo = Vehiculos.query.get(vehiculo_id)

    if vehiculo is None:
        return jsonify({"mensaje": "Vehiculo no encontrado"}), 404 # Devuelve un mensaje si el vehículo no se encuentra

    return jsonify(vehiculo.serialize()), 200


"""--------------------------_<favoritos>_--------------------------------"""

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
