#!/usr/bin/python3
'''places_amenities module'''

from api.v1.views import app_views
from models import storage, storage_t
from flask import abort, jsonify


@app_views.route(
                '/places/<place_id>/amenities',
                methods=['GET'], strict_slashes=False)
def get_places_amenities(place_id):
    '''Retrieves the list of all Amenity objects of a Place'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    amenities = []
    if storage_t == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [
            storage.get("Amenity", amenity_id).to_dict()
            for amenity_id in place.amenity_ids
        ]

    return jsonify(amenities)


@app_views.route(
                '/places/<place_id>/amenities/<amenity_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_amenity_to_place(place_id, amenity_id):
    '''endpoint that deletes an Amenity object to a Place'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)

    storage.save()
    return jsonify({})


@app_views.route(
                '/places/<place_id>/amenities/<amenity_id>',
                methods=['POST'],
                strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    '''endpoint that unliks an Amenity object from a Place object'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict())
        place.amenity_ids.append(amenity.id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
