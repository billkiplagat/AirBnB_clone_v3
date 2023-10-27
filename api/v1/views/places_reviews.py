#!/usr/bin/python3
""" REST api for the Review module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models import storage


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves all reviews """
    if storage.get('Place', place_id) is None:
        abort(404)
    reviews_dict = storage.all('Review')
    reviews_list = [
        review.to_dict()
        for review in reviews_dict.values()
        if review.place_id == place_id
    ]
    return jsonify(reviews_list)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """ Retrieves a single Review using its id """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review = review.to_dict()
    return jsonify(review)


@app_views.route('/reviews/<string:review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """ Deletes a Review using its id """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review.delete()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new Review """
    if storage.get('Place', place_id) is None:
        abort(404)
    if request.json is None:
        return 'Not a JSON', 400
    fields = request.get_json()
    user_id = fields.get('user_id')
    if user_id is None:
        return 'Missing user_id', 400
    if storage.get('User', user_id) is None:
        abort(404)
    if fields.get('text') is None:
        return 'Missing text', 400
    review = Review(**fields)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """ Updates a Review using its id """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if request.json is None:
        return 'Not a JSON', 400
    fields = request.get_json()
    for key, value in fields.items():
        if key not in ('id', 'user_id', 'place_id',
                       'created_at', 'updated_at'):
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
