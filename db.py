import os
import urlparse

import oursql


url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
conn = oursql.connect(
    host=url.hostname, user=url.username, passwd=url.password)
cursor = conn.cursor(oursql.DictCursor)


def authenticate(email, password):
    return cursor.execute(
        'SELECT * FROM user WHERE email = ? AND password = ? LIMIT 1',
        (email, password))


def get_user_profile(user_id):
    return cursor.execute(
        'SELECT * FROM profile WHERE profile.user_id = ?',
        (user_id))
