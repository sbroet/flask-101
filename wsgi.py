# wsgi.py
# pylint: disable=missing-docstring


from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World! this is a test"

@app.route('/api/v1/products')
def product():
    PRODUCTS = {1: { 'id': 1, 'name': 'Skello' },2: { 'id': 2, 'name': 'Socialive.tv' }}
    #return "producti is "
    #return jsonify(PRODUCTS[1])
    return jsonify(list(PRODUCTS.values()))
