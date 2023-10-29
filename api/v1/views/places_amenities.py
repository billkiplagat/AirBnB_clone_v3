#!/usr/bin/python3
""" REST api for the Amenity module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/places/<string:place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """ Retrieves all amenities """
    if storage.get('Place', place_id) is None:
        abort(404)
    amenities_dict = storage.all('Amenity')
    amenities_list = [
        amenity.to_dict()
        for amenity in amenities_dict.values()
        if amenity.place_id == place_id
    ]
    return jsonify(amenities_list)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """ Retrieves a single Amenity using its id """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """ Deletes a Amenity using its id """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity(place_id):
    """ Creates a new Amenity """
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
    amenity = Amenity(**fields)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """ Updates a Amenity using its id """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if request.json is None:
        return 'Not a JSON', 400
    fields = request.get_json()
    for key, value in fields.items():
        if key not in ('id', 'user_id', 'place_id',
                       'created_at', 'updated_at'):
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
