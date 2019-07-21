from flask import Blueprint
from flask_restful import Resource, Api

blueprint = Blueprint('users', __name__)
api = Api(blueprint)

class UsersPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong'
        }

api.add_resource(UsersPing, '/users/ping')

