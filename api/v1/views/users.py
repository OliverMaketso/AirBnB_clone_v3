#!/usr/bin/python3
"""A module for viewing User objects."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users')
def get_users():
    """Retrieves all user objects"""
    users = [obj.to_dict() for obj in storage.all("User").values()]

    return jsonify(users)


@app_views.route('/users/<user_id>')
def get_specific_user(user_id):
    """Retrieves a specific user wrt id"""
    user = [obj.to_dict() for obj in storage.all("User").values()
            if obj.id == user_id]

    if not user:
        abort(404)

    return jsonify(user[0])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """Deletes a specific user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def new_user():
    """Creates a new instance of user object"""
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    if 'email' not in req_data:
        abort(400, "Missing email")
    if 'password' not in req_data:
        abort(400, "Missing password")

    new_user = User(email=req_data['email'], password=req_data['password'])
    storage.new(new_user)
    storage.save()

    user = []
    user.append(new_user.to_dict())

    return jsonify(user[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates the values of an User object"""
    users = storage.all("User").values()
    user = [obj.to_dict() for obj in users
            if obj.id == user_id]

    if not user:
        abort(404)

    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")

    for obj in users:
        if obj.id == user_id:
            obj.first_name = req_data['first_name']
            obj.last_name = req_data['last_name']
            obj.password = req_data['password']

    storage.save()

    return jsonify(user[0]), 200