#!/usr/bin/python3
'''amenities view module'''

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, request, make_response


@app_views.route('/amenities', strict_slashes=False)
def get_all_amenities():
    '''endpoint that retrieves all amenities'''
    amenities = storage.all("Amenity")
    result = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(result)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_single_amenity(amenity_id):
    '''retrieves a single amenity with the particular id'''
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route(
                '/amenities/<amenity_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_amenity(amenity_id):
    '''endpoint that deletes a single amenity'''
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''an endpoint that create a new amenity'''
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    amenity = Amenity(**data)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    '''an endpoint that update an existing amenity'''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ["id", "created_at", "updated_at"]
    for key in data:
        if key not in ignore_keys:
            setattr(amenity, key, data[key])

    storage.save()
    return jsonify(amenity.to_dict()), 200
