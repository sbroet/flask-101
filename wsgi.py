# wsgi.py
# pylint: disable=missing-docstring
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

import itertools

from flask import Flask, jsonify, abort, request
app = Flask(__name__)

# Prefix api path using a version number is really important to manage future breaking evolutions
# This way, we can continue to offer the old service using /v1 url and offer the new one using /v2
# We will remove /v1 api (and related code) when all our users will use /v2 url.
BASE_URL = '/api/v1'

# Remember this is only a really simple database simulation.
# This data is only persisted in RAM : if you restart your server, modifications are lost.
# Don't worry about this, our goal for today is to understand REST api, not to really persist data.
PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv' },
    3: { 'id': 3, 'name': 'Le Wagon'},
}

# This is a simple naive way to generate consecutive id (like a database will do)
START_INDEX = len(PRODUCTS) + 1
IDENTIFIER_GENERATOR = itertools.count(START_INDEX)


@app.route(f'{BASE_URL}/products', methods=['GET'])
def read_many_products():
    products = list(PRODUCTS.values())

    # Returns a tuple corresponding to flask.Response constructor arguments
    # Cf: https://flask.palletsprojects.com/en/1.1.x/api/?highlight=response#flask.Response
    # By default, 2nd argument is 200 (but we want to be explicit while learning concepts)
    return jsonify(products), 200  # OK


@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['GET'])
def read_one_product(product_id):
    product = PRODUCTS.get(product_id)

    if product is None:
        abort(404)

    return jsonify(product), 200  # OK


@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['DELETE'])
def delete_one_product(product_id):
    product = PRODUCTS.pop(product_id, None)

    if product is None:
        abort(404)  # No product of product_id found is a Not Found Error

    # If 204, 1st argument (body) is ignored
    # We can put anything we want in 1st argument (but we want to be explicit to make our code more maintenable)
    # '' or None are common used values to explicit this case
    #
    # Delete action (DELETE method) no need to return the entity since we removed this entity
    return '', 204  # No Content


# No product_id in create (POST method) url since it is the database which implements the id counter
# If api consumers could choose an id, it would lead to many erros :
#  - race condition for a given id choosed by many users
#  - how to know which is is not used for now
#  - database can optimize ids management because they know the way they are created
@app.route(f'{BASE_URL}/products', methods=['POST'])
def create_one_product():
    data = request.get_json()

    if data is None:
        abort(400)  # Missing needed field(s) is a Bad Request Error

    name = data.get('name')

    if name is None:
        abort(400)  # Missing needed field is a Bad Request Error

    if name == '' or not isinstance(name, str):
        abort(422)  # Bad format for needed field is a Unprocessable Entity Error

    next_id = next(IDENTIFIER_GENERATOR)
    PRODUCTS[next_id] = {'id' : next_id , 'name' : name }

    # We need to return the entire entity to comunicate the new id to the api consumer
    # This way, he can act on this resource using his id.
    #
    # We could simply return the id, but it's not in the REST spirit
    # => Don't forget : /<entity>/<entity_id> represents an entire entity
    return jsonify(PRODUCTS[next_id]), 201  # Created


@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['PATCH'])
def update_one_product(product_id):
    data = request.get_json()
    if data is None:
        abort(400)

    name = data.get('name')

    if name is None:
        abort(400)

    if name == '' or not isinstance(name, str):
        abort(422)

    product = PRODUCTS.get(product_id)

    if product is None:
        abort(404)

    PRODUCTS[product_id]['name'] = name

    # Update action (UPDATE method) no need to return the entity since we know what we modified
    return '', 204
