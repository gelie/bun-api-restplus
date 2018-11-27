from flask_restplus import Namespace, Resource, fields
from core.models import User

api = Namespace('users', description='User related operations')

user = api.model('User', {
    'user_id': fields.String(required=True, description='The user identifier'),
    'login': fields.String(required=True, description='The user name'),
    # 'links': fields.List(fields.Url('api.user_membership'user_fields), description='The user\'s group memberships')
    'groups': fields.List('user_membership')
})


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user)
    def get(self):
        '''List all users'''
        return User.query.paginate().items


@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserPage(Resource):
    @api.doc('get_user')
    @api.marshal_with(user, skip_none=True)
    def get(self, user_id):
        '''Fetch a user given its identifier'''
        return User.query.get_or_404(user_id)

