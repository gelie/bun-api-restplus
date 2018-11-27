import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://bungeni:bungeni@localhost:3032/bungeni'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
