#!/usr/bin/python3
"""module that creates a new view for review objects
that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models.review import Review
from models import storage
from models.user import User


@app_views.route('/place/<place_id>/reviews')
def reviews_list(place_id):
    """Retrieves the list of all Review objects of a City"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>')
def review_obj(review_id):
    """Retrieves a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'])
def delete(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """Creates a Review"""
    review = []
    req_data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not req_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_data:
        abort(400, 'Missing user_id')

    user = storage.get(User, req_data['user_id'])
    if not user:
        abort(404)

    new_review = Review(user_id=req_data['user_id'], place_id=place_id)
    storage.new(new_review)
    storage.save()
    review.append(new_review.to_dict())
    return jsonify(review[0]), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """Updates a Review object."""
    req_data = request.get_json()

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not req_data:
        abort(400, 'Not a JSON')

    if 'text' in req_data:
        review.text = req_data['text']

    storage.save()
    return jsonify(review.to_dict()), 200