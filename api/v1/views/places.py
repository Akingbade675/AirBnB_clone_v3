#!/usr/bin/python3
'''cities module'''

from api.v1.views import app_views
from models import storage
from models.place import Place
from flask import abort, jsonify, request, make_response


@app_views.route(
                '/cities/<city_id>/places',
                methods=['GET'], strict_slashes=False)
def get_places_in_city(city_id):
    '''Retrieves the list of all Places objects of a City'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route(
                '/places/<place_id>',
                methods=['GET'], strict_slashes=False)
def get_place(place_id):
    '''retrieves a single place with the particular id'''
    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route(
                '/places/<place_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_place(place_id):
    '''endpoint that deletes a single city'''
    place = storage.get("Place", place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
                '/cities/<city_id>/places',
                methods=['POST'], strict_slashes=False)
def create_place_in_city(city_id):
    '''an endpoint that create a new place for a city'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get("User", data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    data['city_id'] = city_id
    place = Place(**data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''an endpoint that update an existing place'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key in data:
        if key not in ignore_keys:
            setattr(place, key, data[key])
    storage.save()
    return jsonify(place.to_dict())


@app_views.route(
                '/places_search',
                methods=['POST'], strict_slashes=False)
def places_search():
    '''retrieves all Place objects depending of the JSON
    in the body of the request'''
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    places = []
    list_cities = []
    if data == []:
        if data.get("states"):
            states = [storage.get("State", s_id) for s_id in data["states"]]
            for state in states:
                list_cities.extend(state.cities)
                places.extend([city.places for city in state.cities])

        if data.get("cities"):
            cities = [storage.get("City", c_id) for c_id in data["cities"]]
            places.extend([city.places for city in cities if city not in list_cities])

        if not places:
            places = storage.all("Place").values()

        if not data.get("amenities"):
            amenities = [storage.get("Amenity", a_id)
                        for a_id in data["amenities"]]
            for place in places:
                places = [place.to_dict() for place in places
                            if any(amenity in place.amenities
                                for amenity in amenities)]

        return jsonify(places)
