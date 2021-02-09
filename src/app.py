"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except:
        return jsonify('Server Error'), 500

@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    user = jackson_family.get_member(id)
    if user:
        return user, 200
    return 404

@app.route('/member/<int:id>', methods=["DELETE"])
def delete_member(id):
    user = jackson_family.delete_member(id)
    if user:
        return jsonify({"done": True}), 200
    
    return jsonify('Bad request'), 404
  

@app.route('/member', methods=["POST"])
def cretate_member():
    try:
        member = {
            "id": request.json["id"],
            "first_name": request.json["first_name"],
            "last_name": "Jackson",
            "age": request.json["age"],
            "lucky_numbers": request.json["lucky_numbers"]
        }
        create = jackson_family.add_member(member)
        if(create == 200):
            return jsonify('All good'), 200

    except ValueError as err:
        return jsonify('Server Error'), 500

    except Exception as err:
        return jsonify('Bad Request'), 405

    except:
        return jsonify('Internal server error'), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)