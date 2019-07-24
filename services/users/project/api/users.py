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

class UsersList(Resource):
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



#        post_data = request.get_json()
#        email = post_data.get('email')
#        username = post_data.get('username') or email
#        user = User(username=username, email=email)
#
#        if not email:
#            response_data = {
#                'message': 'Invalid payload. No "email" key given',
#                'status': 'fail',
#            }
#            return response_data, 400
#        
#        try:
#            user = User.query.filter_by(email=email).first()
#            if not user:
#                user = User(username=username, email=email)
#                db.session.add(user)
#                db.session.commit()
#                response_data = {
#                    'status': 'success',
#                    'message': f'{email} has been added'
#                }
#                return response_data, 201
#            else:
#                response_data = {
#                    'message': 'Invalid email. Given email already exists.',
#                    'status': 'fail',
#                }
#                return response_data, 400
#        except exc.IntegrityError:
#            db.session.rollback()
#            response_data = {
#                'message': 'Invalid username. Given username already exists.',
#                'status': 'fail',
#            }
#            return response_data, 400

api.add_resource(UsersPing, '/users/ping')
api.add_resource(UsersList, '/users')

