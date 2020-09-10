#!/usr/bin/python3
"""
Create new view for City objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def places(city_id):
    """
    Retrieve all places
    """
    cities_id = storage.get("City", city_id)
    if cities_id:
        all_places = [place.to_dict() for place in cities_id.places]
        return jsonify(all_places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_places(place_id):
    """
    Retrieve places by Id
    """
    places_id = storage.get("Place", place_id)
    if places_id:
        return jsonify(places_id.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_places(place_id):
    """
    Deletes a place object by its Id
    """
    places_id = storage.get("Place", place_id)
    if places_id:
        storage.delete(places_id)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


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


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def put_places(place_id):
    """
    Updates a Place object by its Id
    """
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    places_id = storage.get("Place", place_id)
    if places_id:
        for key, value in json_request.items():
            setattr(places_id, key, value)
        storage.save()
        return jsonify(places_id.to_dict()), 200
    else:
        abort(404)
