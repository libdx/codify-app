import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User

class TestUserService(BaseTestCase):
    """ Tests for `users` Service """

    def setUp(self):
        super().setUp()

        user1 = User(username='tom', email='tom@example.com')
        user2 = User(username='jerry', email='jerry@example.com')
        db.session.add_all([user1, user2])
        db.session.commit()

        self.user1 = user1
        self.user2 = user2

    def test_get_all_users(self):
        """ GET /users returns list of all users """

        users = [self.user1, self.user2]

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            payload = data.get('payload')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(payload), 2)
            self.assertEqual(users[0].username, payload[0]['username'])
            self.assertEqual(users[0].email, payload[0]['email'])
            self.assertEqual(users[1].username, payload[1]['username'])
            self.assertEqual(users[1].email, payload[1]['email'])
            self.assertIn('success', data['status'])
    
    def test_get_user(self):
        """ GET /users/:id returns correct user """

        user = self.user1

        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            payload = data.get('payload')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(user.id, payload['id'])
            self.assertEqual(user.email, payload['email'])
            self.assertEqual(user.username, payload['username'])
            self.assertIn('success', data['status'])

    def test_get_user_by_invalid_id(self):
        """ GET /users/:id with invalid id returns as error """

        id = self.user1.id + self.user2.id
        with self.client:
            response = self.client.get(f'/users/{id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_users(self):
        """ GET /users/ping returns correct response """

        with self.client:
            response = self.client.get('/users/ping')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('pong', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user(self):
        """ POST /users creates new user """
        
        username = 'joe'
        email = 'joe.doe@example.com'
        data = json.dumps({
            'username': username,
            'email': email
        })

        with self.client:
            response = self.client.post(
                '/users',
                data=data,
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(username, data['message'])
            self.assertIn(email, data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_without_username(self):
        """ POST /users without username returns an error """

        email = 'joe.doe@example.com'

        data = json.dumps({'email': email})

        with self.client:
            response = self.client.post(
                '/users',
                data=data,
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('username', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_without_email(self):
        """ POST /users without 'email' key returns an error """

        username = 'joe'

        data = json.dumps({'username': username})

        with self.client:
            response = self.client.post(
                '/users',
                data=data,
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('email', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """ POST /users returns an error if given email already exists """

        username1 = 'joe'
        username2 = 'jane'
        email = 'joe.doe@example.com'

        data1 = json.dumps({
            'username': username1,
            'email': email
        })

        data2 =  json.dumps({
            'username': username2,
            'email': email
        })

        with self.client:
            self.client.post(
                '/users',
                data=data1,
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=data2,
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('email', data['message'])
            self.assertIn('exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_username(self):
        """ POST /users returns an error if given username already exists """

        username = 'joe'
        email1 = 'joe.doe@example.com'
        email2 = 'jane.doe@example.com'

        data1 = json.dumps({
            'username': username,
            'email': email1
        })

        data2 =  json.dumps({
            'username': username,
            'email': email2
        })

        with self.client:
            self.client.post(
                '/users',
                data=data1,
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=data2,
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('username', data['message'])
            self.assertIn('exists', data['message'])
            self.assertIn('fail', data['status'])

if __name__ == '__main__':
    unittest.main()

