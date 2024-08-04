#!/usr/bin/python3
"""A module for viewing State objects."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def statesList():
    """Returns the list of all State objects"""
    states_list = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def stateID(state_id):
    """Returns state object according to ID"""
    states = storage.all("State").values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if not state:
        abort(404)
    return jsonify(state[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """Deletes a State Object with a specific ID"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def post():
    """Performs a POST operation on State."""
    state = []
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    if 'name' not in req_data:
        abort(400, 'Missing name')
    new_state = State(name=req_data['name'])
    storage.new(new_state)
    storage.save()
    state.append(new_state.to_dict())
    return jsonify(state[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put(state_id):
    """Perform a PUT operation on State."""
    states = storage.all("State").values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state[0]['name'] == request.json['name']
    for obj in states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state[0]), 200