import unittest
from flask import Flask, url_for
from flask_testing import TestCase
from app import app, mongo, User, generate_password_hash

class TestFlaskApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config["MONGO_URI"] = "mongodb://localhost:27017/test_database"

        return app

    def setUp(self):
        # Clear the test database
        mongo.db.users.delete_many({})

    def tearDown(self):
        pass

    def test_register_route(self):
        response = self.client.post('/register', data={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User created! Please login.', response.data)

if __name__ == '__main__':
    unittest.main()