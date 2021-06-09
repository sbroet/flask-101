# tests/test_views.py
from flask_testing import TestCase
from wsgi import app

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_read_many_products(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.

    def test_read_one_products(self):
        response = self.client.get("/api/v1/products/1")
        product = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(product, dict)
        self.assertEqual(product['name'], 'Skello')

    def test_read_one_product_not_found(self):
        response = self.client.get("/api/v1/products/20")
        product = response.json
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(product)

    def test_delete_product(self):
        delete_response = self.client.delete("/api/v1/products/3")
        deleted_product = delete_response.json
        self.assertEqual(delete_response.status_code, 204)
        self.assertIsNone(deleted_product)

        read_one_response = self.client.get("/api/v1/products/3")
        read_one_product = read_one_response.json
        self.assertEqual(read_one_response.status_code, 404)
        self.assertIsNone(read_one_product)

    def test_delete_product_not_found(self):
        response = self.client.delete("/api/v1/products/20")
        product = response.json
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(product)

    def test_create_product(self):
        response = self.client.post("/api/v1/products", json={'name': 'Netflix'})
        product = response.json
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(product, dict)
        self.assertEqual(product['name'], 'Netflix')

    def test_create_product_validation_error(self):
        response_1 = self.client.post("/api/v1/products", json={'name': 2})
        product_1 = response_1.json
        self.assertEqual(response_1.status_code, 422)
        self.assertIsNone(product_1)

        response_2 = self.client.post("/api/v1/products", json={'name': ''})
        product_2 = response_2.json
        self.assertEqual(response_2.status_code, 422)
        self.assertIsNone(product_2)

    def test_create_product_bad_request(self):
        response_1 = self.client.post("/api/v1/products", json={'other': 2})
        product_1 = response_1.json
        self.assertEqual(response_1.status_code, 400)
        self.assertIsNone(product_1)

        response_2 = self.client.post("/api/v1/products", json={'other': 'what'})
        product_2 = response_2.json
        self.assertEqual(response_2.status_code, 400)
        self.assertIsNone(product_2)

        response_3 = self.client.post("/api/v1/products")
        product_3 = response_3.json
        self.assertEqual(response_3.status_code, 400)
        self.assertIsNone(product_3)

    def test_update_product(self):
        update_response = self.client.patch("/api/v1/products/1", json={'name': 'Netlify'})
        update_product = update_response.json
        self.assertEqual(update_response.status_code, 204)
        self.assertIsNone(update_product)

        read_response = self.client.get("/api/v1/products/1")
        product = read_response.json
        self.assertEqual(read_response.status_code, 200)
        self.assertIsInstance(product, dict)
        self.assertEqual(product['name'], 'Netlify')

    def test_update_product_not_found(self):
        response = self.client.patch("/api/v1/products/20", json={'name': 'Doctolib'})
        product = response.json
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(product)

    def test_update_product_validation_error(self):
        response_1 = self.client.patch("/api/v1/products/1", json={'name': 2})
        product_1 = response_1.json
        self.assertEqual(response_1.status_code, 422)
        self.assertIsNone(product_1)

        response_2 = self.client.patch("/api/v1/products/1", json={'name': ''})
        product_2 = response_2.json
        self.assertEqual(response_2.status_code, 422)
        self.assertIsNone(product_2)

    def test_update_product_bad_request(self):
        response_1 = self.client.patch("/api/v1/products/1", json={'other': 'what'})
        product_1 = response_1.json
        self.assertEqual(response_1.status_code, 400)
        self.assertIsNone(product_1)

        response_2 = self.client.patch("/api/v1/products/1")
        product_2 = response_2.json
        self.assertEqual(response_2.status_code, 400)
        self.assertIsNone(product_2)
