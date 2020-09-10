#!/usr/bin/python3
"""places_reviews module"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """get all places information from a city"""
    place_dic = storage.get(Place, place_id)
    if place_dic is None:
        abort(404)
    rev_list = []
    for value in place_dic.reviews:
        rev_list.append(value.to_dict())
    return jsonify(rev_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """get information for specified place"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a place based on its review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return (jsonify({})), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """Create a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    jsonRequest = request.get_json()
    if not jsonRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in jsonRequest.keys():
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, jsonRequest["user_id"])
    if not user:
        abort(404)
    if 'text' not in jsonRequest.keys():
        return jsonify({'error': "Missing text"}), 400

    review = Review(place_id=place_id, **jsonRequest)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a place object based on review_id"""
    jsonRequest = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not jsonRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    for attr, val in jsonRequest.items():
        setattr(review, attr, val)
    review.save()
    return jsonify(review.to_dict()), 200
