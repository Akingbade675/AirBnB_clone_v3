#!/usr/bin/python3
'''user view module'''

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, request, make_response


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    '''endpoint that retrieves all users'''
    users = storage.all("User")
    result = [user.to_dict() for user in users.values()]
    return jsonify(result)


@app_views.route('/users/<string:user_id>', strict_slashes=False)
def get_single_user(user_id):
    '''retrieves a single user with the particular id'''
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route(
                '/users/<string:user_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_user(user_id):
    '''endpoint that deletes a single user'''
    user = storage.get("User", user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''an endpoint that create a new user'''
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'email' not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route(
                '/users/<string:user_id>',
                methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''an endpoint that update an existing user'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key in data:
        if key not in ignore_keys:
            setattr(user, key, data[key])

    storage.save()
    return jsonify(user.to_dict())
