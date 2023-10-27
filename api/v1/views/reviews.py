#!/usr/bin/python3
""" REST api for the Review module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models import storage


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    """ Retrieves all reviews """
    reviews_dict = storage.all('Review').values()
    reviews_list = [
        review.to_dict()
        for review in reviews_dict
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


@app_views.route('/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review():
    """ Creates a new Review """
    if request.json is None:
        return 'Not a JSON', 400
    fields = request.get_json()
    if fields.get('name') is None:
        return 'Missing name', 400
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
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
