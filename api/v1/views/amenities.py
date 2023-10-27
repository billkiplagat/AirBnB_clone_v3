#!/usr/bin/python3
""" REST api for the Amenity module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves all amenities """
    amenities_dict = storage.all('Amenity').values()
    amenities_list = [
        amenity.to_dict()
        for amenity in amenities_dict
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
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity(amenity_id):
    """ Creates a new Amenity """
    if request.json is None:
        return 'Not a JSON', 400
    fields = request.get_json()
    if fields.get('name') is None:
        return 'Missing name', 400
    amenity = Amenity(fields)
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
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
