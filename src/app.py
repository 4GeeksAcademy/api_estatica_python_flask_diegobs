"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200


# Para obtener uin miembro por ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "El ID indicado no corresponde a ningún miembro"}), 404


# Para agregar un nuevo miembro
@app.route('/members/new', methods=['POST'])
def add_member():
    request_body = request.get_json()
    if request_body:
        jackson_family.add_member(request_body)
        return jsonify({"msg" : "Se ha añadido el miembro correctamente"}), 200
    else:
        return jsonify({"error" : "Error al añadir el miembro"}), 400
    
    
# Para eliminar un miembro existente
@app.route('/members/delete/<int:id>', methods=['DELETE'])
def delete_member(id):
    jackson_family.delete_member(id)
    return jsonify({"msg" : f"Se ha eliminado el miembro con el ID {id}"}), 200   ## Preguntar cómo añadir otro mensaje en caso de error (Siempre salta el mismo mensaje aunque no borre nada)


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
