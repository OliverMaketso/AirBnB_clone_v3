#!/usr/bin/python3
"""A module for viewing Amenities objects."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities')
def get_amenities():
    """Retrieves all amenity objects"""
    amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>')
def get_specific_amenity(amenity_id):
    """Retrieves a specific amenity wrt id"""
    amenity = [obj.to_dict() for obj in storage.all("Amenity").values()
               if obj.id == amenity_id]

    if not amenity:
        abort(404)

    return jsonify(amenity[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    """Deletes a specific amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def new_amenity():
    """Creates a new instance of amenity object"""
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    if 'name' not in req_data:
        abort(400, "Missing name")
    new_amenity = Amenity(name=req_data['name'])
    storage.new(new_amenity)
    storage.save()

    amenity = []
    amenity.append(new_amenity.to_dict())

    return jsonify(amenity[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates the values of an Amenity object"""
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
               if obj.id == amenity_id]

    if not amenity:
        abort(404)

    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")

    for obj in amenities:
        if obj.id == amenity_id:
            obj.name = req_data['name']

    storage.save()

    return jsonify(amenity[0]), 200