from marshmallow import fields

from core import ma
from core.models import User, Group, UserGroupMembership


class GroupSchema(ma.ModelSchema):
    class Meta:
        model = Group
        fields = ('short_name', 'full_name', '_links')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.group', group_id='<group_id>', _external=1),
        'collection': ma.URLFor('api.groups', _external=1),
        'members': [],
        'sittings': []
    })


class UserMembership(ma.ModelSchema):
    class Meta:
        model = UserGroupMembership
        fields = ('group', 'links')

    links = ma.Hyperlinks({
        'self': ma.URLFor('api.group', group_id='<group_id>', _external=1),
        # 'collection': ma.URLFor('api.groups', _external=1)
    })


class UserSchema(ma.ModelSchema):
    class Meta:
        ordered = True
        model = User
        fields = ('first_name', 'last_name', 'email', 'group_count', 'links')

    group_count = fields.Function(lambda obj: len(obj.user_memberships))
    # pagination_links = fields.Method('get_pagination_links')
    # group_count = fields.Method('get_count')
    # mygroups = fields.Method('get_group_count')
    links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_user', user_id='<user_id>', _external=1),
        'collection': ma.URLFor('api.get_users', _external=1),
        # 'groups': ma.URLFor('api.usergroups', user_id='<user_id>', _external=True)
    })

    def get_pagination_links(self, obj):
        return {
            "next": obj.next
        }

    def get_group_count(self, obj):
        return len(obj.user_memberships)
