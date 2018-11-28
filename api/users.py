from flask import jsonify
from marshmallow import fields
from webargs.flaskparser import use_kwargs

from core.models import User
from . import api
from .schema import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

pagination = {
    'page': fields.Int(missing=1, location="query"),
    'per_page': fields.Int(missing=10, location="query")
}

filter = {
    'login': fields.String(missing=None, location="query")
}


@api.route('/users/', methods=['GET'])
@use_kwargs(filter)
@use_kwargs(pagination)
# @use_args(user_schema)
def get_users(page, per_page, **kwargs):
    """List all users"""
    # only = args["fields"]#, None)
    # print(only)
    filter = {}
    for k, v in kwargs.items():
        filter[k] = v
    print(filter)
    if filter.items():
        users = User.query.filter(filter.items()).paginate(page, per_page, False).items
    else:
        users = User.query.paginate(page, per_page, False).items
    result = users_schema.dump(users)
    return jsonify(result.data)
    # for user in users:
    #     if user.image is not None:
    #         user.image = b64encode(user.image)
    # # return jsonify(users_schema.dump(users).data)
    # return users_schema.dump(users).data


@api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Fetch a user given its identifier"""
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user).data)
