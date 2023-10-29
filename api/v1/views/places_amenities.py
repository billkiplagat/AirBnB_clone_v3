#!/usr/bin/python3
""" REST api for the Amenity module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage, storage_t


@app_views.route('/places/<string:place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """ Retrieves all amenities linked to a place """
    if storage.get('Place', place_id) is None:
        abort(404)
    amenities_dict = storage.all('Amenity')
    amenities_list = [
        amenity.to_dict()
        for amenity in amenities_dict.values()
        if amenity.place_id == place_id
    ]
    return jsonify(amenities_list)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(place_id, amenity_id):
    """ Deletes a Amenity using its id and its place id """
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None or amenity is None:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            break
    else:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity(place_id, amenity_id):
    """ Links an Amenity to a Place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if storage_t == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    place.save()
    amenity.save()
    return jsonify(amenity.to_dict()), 201
