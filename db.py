import os
import re
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

def get_admin_report_friends():
    return cursor.execute(
          'SELECT  users.user_id, GROUP_CONCAT(friend) \
           FROM users LEFT OUTER JOIN friend_of \
           ON friend_of.friend_owner = users.user_id \
           GROUP BY users.user_id;'
          )

def get_admin_report_comments():
    return cursor.execute(
           'SELECT  users.user_id, GROUP_CONCAT(content) \
            FROM users LEFT OUTER JOIN comments_on \
            ON comments_on.user_id = users.user_id \
            LEFT OUTER JOIN  comments \
            ON comments.comment_id = comments_on.comment_id \
            GROUP BY users.user_id;'
           )

def get_admin_report_posts():
    return cursor.execute(
           'SELECT  users.user_id, GROUP_CONCAT(title), GROUP_CONCAT(text_body) \
            FROM users LEFT OUTER JOIN creates_post \
            ON creates_post.user_id = users.user_id \
            LEFT OUTER JOIN post \
            ON post.post_id = creates_post.post_id \
            GROUP BY users.user_id;'
           )

def get_admin_report_gposts():
    return cursor.execute(
           'SELECT  users.user_id, GROUP_CONCAT(title), GROUP_CONCAT(text_body) \
            FROM users LEFT OUTER JOIN create_content \
            ON create_content.user_id = users.user_id \
            LEFT OUTER JOIN group_post \
            ON group_post.gpost_id = create_content.gpost_id \
            GROUP BY users.user_id;' 
           )

def add_friend(friend_owner_id, friend_id, category):
    return cursor.execute('INSERT INTO friend_of VALUES (?, ?, ?)',
                          (friend_owner_id, friend_id, category))

def remove_friend(friend_owner_id, friend_id):
    return cursor.execute('DELETE FROM friend_of WHERE friend_owner = ? \
                          AND friend = ?', (friend_owner_id, friend_id))
