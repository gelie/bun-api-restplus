from base64 import b64encode

from core.models import User
from . import api
from .schema import UserSchema

from flask import jsonify

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@api.route('/users/', methods=['GET'])
# @api.marshal_list_with(users_schema)
def get_users():
    '''List all users'''
    # return jsonify(dict(name='Gavin', surname='Elie'))
    users = User.query.paginate(1, 10, False).items
    for user in users:
        if user.image is not None:
            user.image = b64encode(user.image)
    return jsonify(users_schema.dump(users).data)


@api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # @api.marshal_with(user_schema, skip_none=True)

    '''Fetch a user given its identifier'''
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user).data)
