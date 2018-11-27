# from flask_restplus import Namespace, Resource, fields
# from flask import url_for, jsonify
#
# from core.models import Group
# from .schema import GroupSchema
# from base64 import b64encode
#
# api = Namespace('groups', description='Group related operations')
#
# group_schema = GroupSchema()
# groups_schema = GroupSchema(many=True)
#
# @api.route('/', endpoint='groups')
# class GroupList(Resource):
#     @api.doc('groups')
#     # @api.marshal_list_with(groups_schema)
#     def get(self):
#         '''List all groups'''
#         groups = Group.query.paginate(1, 10, False).items
#         return jsonify(groups_schema.dump(groups).data)
#
#
# @api.route('/<group_id>', endpoint='group')
# @api.param('group_id', 'The group identifier')
# @api.response(404, 'Group not found')
# class GroupPage(Resource):
#     @api.doc('get_group')
#     # @api.marshal_with(group_schema, skip_none=True)
#     def get(self, group_id):
#         '''Fetch a group given its identifier'''
#         group = Group.query.get_or_404(group_id)
#         return jsonify(group_schema.dump(group).data)
#
# # thegroup = api.model('Group', {
#     # 'group_id': fields.String(required=True, description='The group identifier'),
#     # 'full_name': fields.String(required=True, description='The group name'),
# # })
#
#
# # @api.route('/')
# # class GroupList(Resource):
#     # @api.doc('list_groups')
#     # @api.marshal_list_with(thegroup)
#     # def get(self):
#         # '''List all groups'''
#         # return Group.query.paginate().items
#
#
# # @api.route('/<group_id>')
# # @api.param('group_id', 'The group identifier')
# # @api.response(404, 'Group not found')
# # class GroupPage(Resource):
#     # @api.doc('get_group')
#     # @api.marshal_with(thegroup, skip_none=True)
#     # def get(self, group_id):
#         # '''Fetch a group given its identifier'''
#         # return Group.query.get_or_404(group_id)
