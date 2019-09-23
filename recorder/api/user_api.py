from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from recorder.models.user import  User


class UserList(Resource):

    def get(self):
        users = User.get_user_list()
        return [u.as_dict() for u in users]