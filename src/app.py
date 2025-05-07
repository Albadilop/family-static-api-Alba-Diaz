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
def handle_get_all_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"family": members}
    if members is None:
        return jsonify({"error": "Members not found"}), 404
    internal_error= False
    if internal_error:
        return jsonify({"error": "Server error"}), 500
    return jsonify(response_body), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def handle_get_one_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    internal_error= False
    if internal_error:
        return jsonify({"error": "Server error"}), 500
    return jsonify(member), 200


@app.route('/members', methods=['POST'])
def handle_add_member():
    request_body = request.json
    new_member = jackson_family.add_member(request_body)
    if new_member is None:
        return jsonify({"error": "Invalid data"}), 400
    internal_error= False
    if internal_error:
        return jsonify({"error": "Server error"}), 500
    return jsonify(new_member), 201

@app.route('/members/<int:member_id>', methods=['DELETE'])
def handle_delete_one_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if deleted is None:
        return jsonify({"error": "Member does not exist"}), 404
    internal_error= False
    if internal_error:
        return jsonify({"error": "Server error"}), 500
    return jsonify({"done": True}), 200



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
