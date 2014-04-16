import os
import re
import urlparse

import oursql
from oursql import OperationalError, ProgrammingError


conn = oursql.connect(
    host='localhost', user='root', passwd='root', db='mybook')


def authenticate(cursor, email, password):
    return cursor.execute(
        'SELECT * FROM user WHERE email = ? AND password = ? LIMIT 1',
        (email, password))


def get_user_profile(cursor, user_id):
    return cursor.execute(
        'SELECT * FROM profile WHERE profile.user_id = ?',
        (user_id))


def save_uploaded_image(cursor, image_path, user_id):
    return cursor.execute(
        'UPDATE profile SET profile.profile_pic = ? WHERE profile.user_id = ?',
        (image_path, user_id))


def populate(cursor):
    return exec_sql_file(cursor, 'schema.sql')

def exec_sql_file(cursor, sql_file):
    print "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
            try:
                cursor.execute(statement)
            except (OperationalError, ProgrammingError) as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))

            statement = ""
