import json
import unittest

from project.tests.base import BaseTestCase

class TestUserService(BaseTestCase):
    """ Tests for `users` Service """

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

