import oursql

conn = oursql.connect(
    host='localhost', user='username', passwd='pass', port=3307)

cursor = conn.cursor(oursql.DictCursor)


def authenticate(email, password):
    return cursor.execute(
        'SELECT * FROM user WHERE email = ? AND password = ? LIMIT 1',
        (email, password))
