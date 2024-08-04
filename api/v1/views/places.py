#!/usr/bin/python3
"""module that creates a new view for Place objects
that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models import storage
from models.user import User


@app_views.route('/cities/<city_id>/places')
def places_list(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>')
def place_obj(place_id):
    """Retrieves a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'])
def delete(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """Creates a Place"""
    place = []
    req_data = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not req_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_data:
        abort(400, 'Missing user_id')
    if 'name' not in req_data:
        abort(400, 'Missing name')

    # Retrieve the User object with the given user_id
    user = storage.get(User, req_data['user_id'])
    if not user:
        abort(404)

    # Create the new Place object
    new_place = Place(name=req_data['name'], user_id=req_data['user_id'],
                      city_id=city_id)
    storage.new(new_place)
    storage.save()
    place.append(new_place.to_dict())
    return jsonify(place[0]), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """Updates a Place object."""
    req_data = request.get_json()

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not req_data:
        abort(400, 'Not a JSON')

    # Update the attributes of the Place object
    if 'name' in req_data:
        place.name = req_data['name']
    if 'description' in req_data:
        place.description = req_data['description']
    if 'number_rooms' in req_data:
        place.number_rooms = req_data['number_rooms']
    if 'number_bathrooms' in req_data:
        place.number_bathrooms = req_data['number_bathrooms']
    if 'max_guest' in req_data:
        place.max_guest = req_data['max_guest']
    if 'price_by_night' in req_data:
        place.price_by_night = req_data['price_by_night']
    if 'latitude' in req_data:
        place.latitude = req_data['latitude']
    if 'longitude' in req_data:
        place.longitude = req_data['longitude']

    # Save the changes to the storage
    storage.save()

    # Return the updated Place object as JSON
    return jsonify(place.to_dict()), 200