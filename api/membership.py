# from flask_restplus import Namespace, Resource, fields
# from core.models import UserGroupMembership
# from .schema import UserSchema, GroupSchema, UserMembership
# # from .groups import thegroup
#
# user_schema = UserSchema()
# group_schema = GroupSchema
#
# api = Namespace('membership', description='Membership related operations')
#
# @api.route('/user/<int:user_id>', endpoint='usergroups')
# @api.param('user_id', 'The user identifier')
# @api.response(404, 'User not found')
# class UserGroupList(Resource):
#     @api.doc('list_groups_for_user')
#     @api.marshal_list_with(group_schema)
#     def get(self, user_id):
#         '''List a user's groups'''
#         return UserGroupMembership.query.filter(UserGroupMembership.user_id==user_id).paginate().items
#
#
# @api.route('/group/<int:group_id>', endpoint='groupmembers')
# @api.param('group_id', 'List all members of a group')
# @api.response(404, 'Group not found')
# class GroupMemberList(Resource):
#     @api.doc('get_user')
#     @api.marshal_with(user_schema, skip_none=True)
#     def get(self, group_id):
#         '''List a group's members'''
#         # return User.query.get_or_404(group_id)
#         return UserGroupMembership.query.filter(UserGroupMembership.group_id==group_id).paginate().items
