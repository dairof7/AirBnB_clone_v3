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


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def post_places(city_id):
    """
    Creates a Place object
    """
    cities_id = storage.get("City", city_id)
    if cities_id is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'user_id' not in json_request:
        return jsonify({'error': 'Missing user_id'}), 400
    user_id = request.get_json()['user_id']
    users_id = storage.get("User", user_id)
    if users_id is None:
        abort(404)
    if 'name' not in json_request:
        return jsonify({'error': 'Missing name'}), 400
    else:
        new_place = Place(**json_request)
        new_place.city_id = city_id
        new_place.user_id = user_id
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


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
