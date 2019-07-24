from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc

from project import db
from project.api.models import User

blueprint = Blueprint('users', __name__)
api = Api(blueprint)

class UsersPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong'
        }

class Users(Resource):
    def get(self, user_id):
        """ Returns single user """
        
        user = User.query.filter_by(id=user_id).first()

        if user:
            return {
                'payload': user.to_json(),
                'status': 'success',
            }, 200
        else:
            return {
                'message': 'Invalid payload',
                'status': 'fail',
            }, 404


class UsersList(Resource):
    def get(self):
        users = User.query.all()

        return {
            'payload': [user.to_json() for user in users],
            'status': 'success',
        }, 200

    def post(self):
        data = request.get_json()

        email = data.get('email')
        username = data.get('username')

        if not email:
            return {
                'message': 'Invalid payload. \'email\' not given',
                'status': 'fail',
            }, 400

        if not username:
            return {
                'message': 'Invalid payload. \'username\' not given',
                'status': 'fail',
            }, 400

        user_by_email = User.query.filter_by(email=email).first()
        user_by_username = User.query.filter_by(username=username).first()

        if not user_by_email and not user_by_username:
            try:
                user = User(username=username, email=email)
                db.session.add(user)
                db.session.commit()

                return {
                    'message': f'User {user.username} with email "{user.email}" has been created',
                    'status': 'success'
                }, 201
            except exc.IntegrityError:
                db.session.rollback()
                return {
                    'message': 'Invalid payload',
                    'status': 'fail'
                }, 400
        elif user_by_email:
            return {
                'message': f'Invalid payload. User with email "{email}" already exists',
                'status': 'fail'
            }, 400
        elif user_by_username:
            return {
                'message': f'Invalid payload. User with username "{username}" already exists',
                'status': 'fail'
            }, 400

api.add_resource(UsersPing, '/users/ping')
api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<user_id>')

