from flask import Blueprint
from flask_restplus import Api

from api.users import api as ns1
from api.groups import api as ns2
from api.membership import api as ns3

blueprint = Blueprint('api', __name__)
api = Api(blueprint)
api.add_namespace(ns1, path='/bungeni/api/v1/users')
api.add_namespace(ns2, path='/bungeni/api/v1/groups')
api.add_namespace(ns3, path='/bungeni/api/v1/membership')
