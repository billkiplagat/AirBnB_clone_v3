#!/usr/bin/python3
""" REST api for the Place module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models import storage


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places_by_city_id(city_id):
    """ Retrieves all places in a city """
    if storage.get('City', city_id) is None:
        abort(404)
    places_dict = storage.all('Place')
    places_list = [
        place.to_dict()
        for place in places_dict.values()
        if place.city_id == city_id
    ]
    return jsonify(places_list)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """ Retrieves a single Place using its id """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place = place.to_dict()
    return jsonify(place)


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """ Deletes a Place using its id """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place.delete()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a new Place """
    if request.json is None:
        return 'Not a JSON', 400
    if storage.get('City', city_id) is None:
        abort(404)
    fields = request.get_json()
    if fields.get('user_id') is None:
        return 'Missing user_id', 400
    user_id = fields.get('user_id')
    if storage.get('User', user_id):
        abort(404)
    if fields.get('name') is None:
        return 'Missing name', 400
    place = Place(**fields)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place_by_id(place_id):
    """ Updates a Place using its id """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.json is None:
        return 'Not a JSON', 400
    fields = request.get_json()
    for key, value in fields.items():
        if key not in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
