#!/usr/bin/python3
"""users module"""

from api.v1.views import app_views
from flask import request, make_response, jsonify, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """"get user information for all users"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get user information for a specified user object based on user id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete(user_id):
    """deletes a single user object based on its user id"""
    user = storage.get(User, user_id)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create (POST) a new user object"""
    json_dict = request.get_json()
    if not json_dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in json_dict:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in json_dict:
        return make_response(jsonify({"error": "Missing password"}), 400)
    user = User(**json_dict)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """updates a user object based on it's id"""
    json_dict = request.get_json()
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not json_dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in json_dict.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
