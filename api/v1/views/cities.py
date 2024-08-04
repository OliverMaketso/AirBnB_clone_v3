#!/usr/bin/python3
"""A module for viewing City objects."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_in_state(state_id):
    """Retrieves a list of city objects in a state"""
    states = storage.all("State").values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if state == []:
        abort(404)
    cities_list = [obj.to_dict() for obj in storage.all("City").values()
                   if state_id == obj.state_id]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>')
def a_city(city_id):
    """Retrieves a specific city"""
    cities_list = storage.all("City").values()
    one_city = [obj.to_dict() for obj in cities_list if obj.id == city_id]
    if one_city == []:
        abort(404)
    return jsonify(one_city[0])


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """Deletes a city object wrt id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """Creates a City object"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    states = storage.all("State").values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]

    if state == []:
        abort(404)

    cities = []
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    cities.append(new_city.to_dict())

    return jsonify(cities[0]), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    cities = storage.all("City").values()
    city = [obj.to_dict() for obj in cities if obj.id == city_id]

    if city == []:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    city[0]['name'] = request.json['name']
    for obj in cities:
        if obj.id == city_id:
            obj.name = request.json['name']
    storage.save()

    return jsonify(city[0]), 200