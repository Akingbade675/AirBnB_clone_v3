#!/usr/bin/python3
'''cities module'''

from api.v1.views import app_views
from models import storage
from models.city import City
from flask import abort, jsonify, request, make_response


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_state_cities(state_id):
    '''Retrieves the list of all City objects of a State'''
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return state.cities


@app_views.route('/cities/<city_id>', strict_slashes=False)
def state(city_id):
    '''retrieves a single city with the particular id'''
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route(
                '/cities/<city_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_state(city_id):
    '''endpoint that deletes a single city'''
    city = storage.get("City", city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city_for_state(state_id):
    '''an endpoint that create a new city for a state'''
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    city = City(**data)
    city.state_id = state_id
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_state(city_id):
    '''an endpoint that update an existing city'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ["id", "created_at", "updated_at"]
    for key in data:
        if key not in ignore_keys:
            setattr(city, key, data[key])
    storage.save()
    return jsonify(city.to_dict()), 200
