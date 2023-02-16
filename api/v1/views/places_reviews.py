#!/usr/bin/python3
'''places_reviews module'''

from api.v1.views import app_views
from models import storage
from models.review import Review
from flask import abort, jsonify, request, make_response


@app_views.route(
                '/places/<place_id>/reviews',
                methods=['GET'], strict_slashes=False)
def get_places_reviews(place_id):
    '''Retrieves the list of all Review objects of a Place'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route(
                '/reviews/<string:review_id>',
                methods=['GET'], strict_slashes=False)
def get_review(review_id):
    '''retrieves a single review with the particular id'''
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route(
                '/reviews/<string:review_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_review(review_id):
    '''endpoint that deletes a single review'''
    review = storage.get("Review", review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
                '/places/<string:place_id>/reviews',
                methods=['POST'], strict_slashes=False)
def create_review_for_place(place_id):
    '''an endpoint that create a new review for a place'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get("User", data['user_id'])
    if not user:
        abort(404)

    if 'text' not in data:
        return make_response(jsonify({"error": "Missing text"}), 400)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route(
                '/reviews/<string:review_id>',
                methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''an endpoint that update an existing review'''
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key in data:
        if key not in ignore_keys:
            setattr(review, key, data[key])
    storage.save()
    return jsonify(review.to_dict())
