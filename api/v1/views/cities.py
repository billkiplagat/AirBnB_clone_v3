#!/usr/bin/python3
""" REST api for the City module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models import storage


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_state_cities_by_id(state_id):
    """ Retrieves all cities in a state using state id """
    if storage.get('State', state_id) is None:
        abort(404)
    cities_dict = storage.all('City')
    cities_list = [
        city.to_dict()
        for city in cities_dict.values()
        if city.state_id == state_id
    ]
    return jsonify(cities_list)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """ Retrieves a single city using its id """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """ Deletes a City using its id """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a new City in a specific State """
    if request.json is None:
        return 'Not a JSON', 400
    if storage.get('State', state_id) is None:
        abort(404)
    fields = request.get_json()
    if fields.get('name') is None:
        return 'Missing name', 400
    city = City(**fields)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city_by_id(city_id):
    """ Updates a City using its id """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.json is None:
        return 'Not a JSON', 400
    fields = request.get_json()
    for key, value in fields.items():
        if key not in ('id', 'state_id', 'created_at', 'updated_at'):
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
