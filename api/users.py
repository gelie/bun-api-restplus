from flask_restplus import Namespace, Resource, fields
from flask import url_for, jsonify

from core.models import User
from .schema import UserSchema
from base64 import b64encode

api = Namespace('users', description='User related operations')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@api.route('/', endpoint='users')
class UserList(Resource):
    @api.doc('list_users')
    # @api.marshal_list_with(UserSchema)
    def get(self):
        '''List all users'''
        users = User.query.paginate(1, 10, False).items
        for user in users:
            if user.image is not None:
                user.image = b64encode(user.image)
        return jsonify(users_schema.dump(users).data)


@api.route('/<user_id>', endpoint='user')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserPage(Resource):
    @api.doc('get_user')
    # @api.marshal_with(user_schema, skip_none=True)
    def get(self, user_id):
        '''Fetch a user given its identifier'''
        user = User.query.get_or_404(user_id)
        return jsonify(user_schema.dump(user).data)
