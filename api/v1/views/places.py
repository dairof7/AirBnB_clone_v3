#!/usr/bin/python3
"""cities.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """get all places information from a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """get information for specified place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place based on its place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return (jsonify({}))


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """Create a Place"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    jsonRequest = request.get_json()
    if not jsonRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in jsonRequest:
        return jsonify({'error': 'Missing name'}), 400
    if 'user_id' not in jsonRequest:
        return jsonify({'error': 'Missing user_id'}), 400
    else:
        user_id = jsonRequest['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)

    obj = Place(**jsonRequest)
    setattr(obj, "city_id", city_id)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())
