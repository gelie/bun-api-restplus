# coding: utf-8
from sqlalchemy import Boolean, CheckConstraint, Column, Date, DateTime, ForeignKey, Integer, LargeBinary, String, Text, UniqueConstraint
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


from core import db

from flask import url_for


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [
                dict(item) for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total},
            '_links': {
                'self': url_for(
                    endpoint,
                    _external=True,
                    page=page,
                    per_page=per_page,
                    **kwargs),
                'next': url_for(
                    endpoint,
                    _external=True,
                    page=page + 1,
                    per_page=per_page,
                    **kwargs) if resources.has_next else None,
                'prev': url_for(
                    endpoint,
                    _external=True,
                    page=page - 1,
                    per_page=per_page,
                    **kwargs) if resources.has_prev else None}}
        return data


class Agenda(db.Model):
    __tablename__ = 'agenda'
    __table_args__ = {'schema': 'public'}

    agenda_id = db.Column(
        db.Integer,
        primary_key=True,
        server_default=db.FetchedValue())
    title = db.Column(db.String(128), nullable=False)
    sitting_id = db.Column(db.ForeignKey('public.sitting.sitting_id'))
    body = db.Column(db.Text)

    sitting = db.relationship(
        'Sitting',
        primaryjoin='Agenda.sitting_id == Sitting.sitting_id',
        backref='agendas')


class Alfie(db.Model):
    __tablename__ = 'alfie'
    __table_args__ = {'schema': 'public'}

    alfie_id = db.Column(
        db.Integer,
        primary_key=True,
        server_default=db.FetchedValue())
    head_id = db.Column(db.ForeignKey('public.doc.doc_id'), index=True)
    alfie_name = db.Column(db.Text, nullable=False)
    alfie_key = db.Column(db.Text, nullable=False)
    alfie_date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(7), nullable=False)
    sitting_id = db.Column(
        db.ForeignKey(
            'public.sitting.sitting_id',
            match='FULL'))

    head = db.relationship(
        'Doc',
        primaryjoin='Alfie.head_id == Doc.doc_id',
        backref='doc_alfies')
    sitting = db.relationship(
        'Sitting',
        primaryjoin='Alfie.sitting_id == Sitting.sitting_id',
        backref='sitting_alfies')


class Country(db.Model):
    __tablename__ = 'country'
    __table_args__ = {'schema': 'public'}

    country_id = db.Column(db.String(2), primary_key=True)
    iso_name = db.Column(db.String(80), nullable=False)
    country_name = db.Column(db.String(80), nullable=False)
    iso3 = db.Column(db.String(3))
    numcode = db.Column(db.Integer)
    language = db.Column(db.String(5), nullable=False)


class Doc(db.Model):
    __tablename__ = 'doc'
    __table_args__ = {'schema': 'public'}

    doc_id = db.Column(db.Integer, primary_key=True)
    parliament_id = db.Column(db.ForeignKey('public.parliament.parliament_id'))
    owner_id = db.Column(db.ForeignKey('public.user.user_id'), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    doc_type = db.Column(db.String(128))
    doc_procedure = db.Column(db.String(128))
    type_number = db.Column(db.Integer)
    registry_number = db.Column(db.String(128))
    uri = db.Column(db.String(1024))
    acronym = db.Column(db.String(48))
    title = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(5), nullable=False)
    body = db.Column(db.Text)
    original_text = db.Column(db.Text)
    status = db.Column(db.String(48), index=True)
    status_date = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.FetchedValue())
    group_id = db.Column(db.ForeignKey('public.group.group_id'))
    subject = db.Column(db.Text)
    coverage = db.Column(db.Text)
    geolocation = db.Column(db.Text)
    head_id = db.Column(db.ForeignKey('public.doc.doc_id'))
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.FetchedValue())
    assignee_id = db.Column(db.Integer)
    sitting_id = db.Column(
        db.ForeignKey('public.sitting.sitting_id'),
        index=True)

    group = db.relationship(
        'Group',
        primaryjoin='Doc.group_id == Group.group_id',
        backref='group_docs')
    head = db.relationship(
        'Doc',
        remote_side=[doc_id],
        primaryjoin='Doc.head_id == Doc.doc_id',
        backref='docs')
    owner = db.relationship(
        'User',
        primaryjoin='Doc.owner_id == User.user_id',
        backref='user_docs')
    parliament = db.relationship(
        'Parliament',
        primaryjoin='Doc.parliament_id == Parliament.parliament_id',
        backref='parliament_docs')
    sitting = db.relationship(
        'Sitting',
        primaryjoin='Doc.sitting_id == Sitting.sitting_id',
        backref='sitting_docs')


class Principal(db.Model):
    __tablename__ = 'principal'
    __table_args__ = {'schema': 'public'}

    principal_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), nullable=False)


class Group(PaginatedAPIMixin, Principal):
    __tablename__ = 'group'
    __table_args__ = {'schema': 'public'}

    group_id = db.Column(
        db.ForeignKey('public.principal.principal_id'),
        primary_key=True)
    short_name = db.Column(db.String(512), nullable=False)
    full_name = db.Column(db.String(1024))
    acronym = db.Column(db.String(32))
    principal_name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(32))
    status_date = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.FetchedValue())
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    sub_type = db.Column(db.String(128))
    parent_group_id = db.Column(db.ForeignKey('public.group.group_id'))
    language = db.Column(db.String(5), nullable=False)
    group_role = db.Column(db.String(256), nullable=False)
    cluster = db.Column(db.Text)
    prefix = db.Column(db.Text)
    custom3 = db.Column(db.Text)
    custom4 = db.Column(db.Text)

    parent_group = db.relationship(
        'Group',
        remote_side=[group_id],
        primaryjoin='Group.parent_group_id == Group.group_id',
        backref='groups')

    def to_dict(self):
        data = {
            'short_name': self.short_name,
            'full_name': self.full_name,
            'principal_name': self.principal_name,
            'status': self.status,
            'status_date': self.status_date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'parent_group_id': self.parent_group_id,
            'language': self.language,
            'group_role': self.group_role,
            '_links': {
                'self': url_for('api.get_group', group_id=self.group_id, _external=True),
                # 'groups': url_for('api.get_group.parent_group', group_id=self.group_id, _external=True)
            }
        }
        return data


class Parliament(Group):
    __tablename__ = 'parliament'
    __table_args__ = {'schema': 'public'}

    parliament_id = db.Column(
        db.ForeignKey('public.group.group_id'),
        primary_key=True)
    parliament_type = db.Column(db.String(30))
    election_date = db.Column(db.Date, nullable=False)


class User(PaginatedAPIMixin, Principal):
    __tablename__ = 'user'
    __table_args__ = (
        db.CheckConstraint("(active_p)::text = ANY (ARRAY[('A'::character varying)::text, ('I'::character varying)::text, ('D'::character varying)::text])"),
        db.CheckConstraint("(gender)::text = ANY (ARRAY[('M'::character varying)::text, ('F'::character varying)::text])"),
        {'schema': 'public'}
    )

    user_id = db.Column(
        db.ForeignKey('public.principal.principal_id'),
        primary_key=True)
    login = db.Column(db.String(80), nullable=False, unique=True)
    salutation = db.Column(db.String(128))
    title = db.Column(db.String(128))
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    middle_name = db.Column(db.String(256))
    email = db.Column(db.String(512), nullable=False)
    gender = db.Column(db.String(1))
    date_of_birth = db.Column(db.Date)
    birth_country = db.Column(db.ForeignKey('public.country.country_id'))
    birth_nationality = db.Column(db.ForeignKey('public.country.country_id'))
    current_nationality = db.Column(db.ForeignKey('public.country.country_id'))
    marital_status = db.Column(db.String(128))
    uri = db.Column(db.String(1024), unique=True)
    date_of_death = db.Column(db.Date)
    type_of_id = db.Column(db.String(1))
    initials = db.Column(db.String(10))
    password = db.Column(db.String(36))
    salt = db.Column(db.String(24))
    description = db.Column(db.Text)
    remarks = db.Column(db.Text)
    image = db.Column(db.LargeBinary)
    active_p = db.Column(db.String(1))
    receive_notification = db.Column(db.Boolean)
    language = db.Column(db.String(5), nullable=False)

    country = db.relationship(
        'Country',
        primaryjoin='User.birth_country == Country.country_id',
        backref='country_users')
    country1 = db.relationship(
        'Country',
        primaryjoin='User.birth_nationality == Country.country_id',
        backref='country1_users')
    country2 = db.relationship(
        'Country',
        primaryjoin='User.current_nationality == Country.country_id',
        backref='country2_users')

    def to_dict(self, include_email=False):
        data = {
            'user_id': self.user_id,
            'login': self.login,
            'first_name': self.first_name,
            'last_name': self.last_name,
            # 'email': self.email,
            # 'group_count': self.groups.count(),
            '_links': {
                'self': url_for('api.get_user', user_id=self.user_id, _external=True),
                'groups': url_for('api.get_groups', user_id=self.user_id),
                # 'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['login', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


class Session(db.Model):
    __tablename__ = 'session'
    __table_args__ = {'schema': 'public'}

    session_id = db.Column(
        db.Integer,
        primary_key=True,
        server_default=db.FetchedValue())
    parliament_id = db.Column(
        db.ForeignKey('public.parliament.parliament_id'),
        nullable=False)
    short_name = db.Column(db.String(512), nullable=False)
    full_name = db.Column(db.String(1024), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    language = db.Column(db.String(5), nullable=False)

    parliament = db.relationship(
        'Parliament',
        primaryjoin='Session.parliament_id == Parliament.parliament_id',
        backref='sessions')


class Sitting(db.Model):
    __tablename__ = 'sitting'
    __table_args__ = {'schema': 'public'}

    sitting_id = db.Column(
        db.Integer,
        primary_key=True,
        server_default=db.FetchedValue())
    group_id = db.Column(
        db.ForeignKey('public.group.group_id'),
        nullable=False)
    session_id = db.Column(db.ForeignKey('public.session.session_id'))
    short_name = db.Column(db.String(512))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    sitting_length = db.Column(db.Integer)
    recurring_id = db.Column(db.Integer)
    recurring_type = db.Column(db.String(32))
    recurring_end_date = db.Column(db.DateTime)
    status = db.Column(db.String(48))
    status_date = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.FetchedValue())
    venue_id = db.Column(db.ForeignKey('public.venue.venue_id'))
    language = db.Column(db.String(5), nullable=False)
    activity_type = db.Column(db.String(1024))
    meeting_type = db.Column(db.String(1024))
    convocation_type = db.Column(db.String(1024))
    cancel_reason = db.Column(db.String(1024))

    group = db.relationship(
        'Group',
        primaryjoin='Sitting.group_id == Group.group_id',
        backref='group_sittings')
    session = db.relationship(
        'Session',
        primaryjoin='Sitting.session_id == Session.session_id',
        backref='session_sittings')
    venue = db.relationship(
        'Venue',
        primaryjoin='Sitting.venue_id == Venue.venue_id',
        backref='venue_sittings')


class UserGroupMembership(db.Model):
    __tablename__ = 'user_group_membership'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'group_id'),
        {'schema': 'public'}
    )

    membership_id = db.Column(
        db.Integer,
        primary_key=True,
        server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('public.user.user_id'), nullable=False)
    group_id = db.Column(
        db.ForeignKey('public.group.group_id'),
        nullable=False)
    status = db.Column(db.String(32))
    status_date = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.FetchedValue())
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    active_p = db.Column(db.Boolean)
    replaced_id = db.Column(
        db.ForeignKey('public.user_group_membership.membership_id'),
        unique=True)
    substitution_type = db.Column(db.String(100))
    membership_type = db.Column(db.String(30), nullable=False)
    language = db.Column(db.String(5), nullable=False)

    group = db.relationship(
        'Group',
        primaryjoin='UserGroupMembership.group_id == Group.group_id',
        backref='group_memberships')
    replaced = db.relationship(
        'UserGroupMembership',
        uselist=False,
        remote_side=[membership_id],
        primaryjoin='UserGroupMembership.replaced_id == UserGroupMembership.membership_id',
        backref='user_group_memberships')
    user = db.relationship(
        'User',
        primaryjoin='UserGroupMembership.user_id == User.user_id',
        backref='user_memberships')


class Venue(db.Model):
    __tablename__ = 'venue'
    __table_args__ = {'schema': 'public'}

    venue_id = db.Column(
        db.Integer,
        primary_key=True,
        server_default=db.FetchedValue())
    short_name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(5), nullable=False)
    group_id = db.Column(db.ForeignKey('public.group.group_id'))

    group = db.relationship(
        'Group',
        primaryjoin='Venue.group_id == Group.group_id',
        backref='venues')
