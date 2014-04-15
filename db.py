import os
import urlparse

import oursql


url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
conn = oursql.connect(
    host=url.hostname, user='b3a1a2017d486e', passwd='3c5b2de6')


def authenticate(cursor, email, password):
    return cursor.execute(
        'SELECT * FROM user WHERE email = ? AND password = ? LIMIT 1',
        (email, password))


def get_user_profile(cursor, user_id):
    return cursor.execute(
        'SELECT * FROM profile WHERE profile.user_id = ?',
        (user_id))


def populate(cursor):
    with open('schema.sql') as schema:
        return cursor.execute(schema.read())
