#!/usr/bin/python3
'''state module'''

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, request, make_response


@app_views.route('/states', strict_slashes=False)
def states():
    '''endpoint that retrieves all states'''
    states = storage.all("State")
    result = [state.to_dict() for state in states.values()]
    return jsonify(result)


@app_views.route('/states/<state_id>', strict_slashes=False)
def state(state_id):
    '''retrieves a single state with the particular id'''
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route(
                '/states/<state_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_state(state_id):
    '''endpoint that deletes a single state'''
    state = storage.get("State", state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    '''an endpoint that create a new state'''
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    state = State(**data)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''an endpoint that update an existing state'''
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ["id", "created_at", "updated_at"]
    for key in data:
        if key not in ignore_keys:
            setattr(state, key, data[key])

    storage.save()
    return jsonify(state.to_dict())
