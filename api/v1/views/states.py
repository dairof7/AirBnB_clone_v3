#!/usr/bin/python3
"""states module"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retreives the list of all the States"""
    states = []
    all_states = storage.all(State).values()
    for state in all_states:
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a single State object by it's id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object by it's id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a new state object with POST"""
    jsonRequest = request.get_json()
    if not jsonRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in jsonRequest:
        return jsonify({'error': 'Missing name'}), 400
    else:
        _state = State(**jsonRequest)
        storage.new(_state)
        storage.save()
        return jsonify(_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Update a state object with PUT"""
    obj = storage.get(State, state_id)
    jsonRequest = request.get_json()
    if not jsonRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    if state_id:
        for key, value in jsonRequest.items():
            setattr(obj, key, value)
        storage.save()
        return make_response(jsonify(obj.to_dict(), 200))
    else:
        abort(404)
