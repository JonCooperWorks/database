import os
import re
import urlparse

import oursql


conn = oursql.connect(
   host='localhost', user='root', passwd='', db='mybook')


def authenticate(cursor, email, password):
    cursor.execute(
      'SELECT * FROM users JOIN profile ON profile.user_id=users.user_id \
       WHERE email = ? AND hpassword = ? LIMIT 1',
      (email, password))
    user = cursor.fetchone()
    if user:
      return user

def get_user_profile(cursor, user_id):
    cursor.execute(
        'SELECT * FROM profile WHERE profile.user_id = ?',
        (user_id))
    user = cursor.fetchone()
    if user:
      return user

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

def get_admin_report_friends(cursor):
    report = cursor.execute(
          'SELECT  users.user_id, GROUP_CONCAT(friend) as friends \
           FROM users LEFT OUTER JOIN friend_of \
           ON friend_of.friend_owner = users.user_id \
           GROUP BY users.user_id;'
          )
    report = cursor.fetchall()
    if report:
      return report

def get_admin_report_comments(cursor):
    report = cursor.execute(
           'SELECT  users.user_id, GROUP_CONCAT(content) as comments \
            FROM users LEFT OUTER JOIN comments_on \
            ON comments_on.user_id = users.user_id \
            LEFT OUTER JOIN  comments \
            ON comments.comment_id = comments_on.comment_id \
            GROUP BY users.user_id;'
           )
    report = cursor.fetchall()
    if report:
      return report

def get_admin_report_posts(cursor):
    report = cursor.execute(
           'SELECT  users.user_id, GROUP_CONCAT(title) as title, GROUP_CONCAT(text_body) as text \
            FROM users LEFT OUTER JOIN creates_post \
            ON creates_post.user_id = users.user_id \
            LEFT OUTER JOIN post \
            ON post.post_id = creates_post.post_id \
            GROUP BY users.user_id;'
           )
    report = cursor.fetchall()
    if report:
      return report

def get_admin_report_gposts(cursor):
    report = cursor.execute(
           'SELECT  users.user_id, GROUP_CONCAT(title) as title, GROUP_CONCAT(text_body) as text \
            FROM users LEFT OUTER JOIN create_content \
            ON create_content.user_id = users.user_id \
            LEFT OUTER JOIN group_post \
            ON group_post.gpost_id = create_content.gpost_id \
            GROUP BY users.user_id;' 
           )
    report = cursor.fetchall()
    if report:
      return report

def get_id_by_email(cursor, email):
    query = 'SELECT user_id FROM profile WHERE profile.email = \'%s\';' % email
    cursor.execute(query)
    user = cursor.fetchone()
    if user:
      return user

def add_friend(cursor, friend_owner_id, friend_id, category):
    cursor.execute('INSERT INTO friend_of VALUES (?, ?, ?)',
                   (friend_owner_id, friend_id, category))
    return True

def remove_friend(friend_owner_id, friend_id):
    return cursor.execute('DELETE FROM friend_of WHERE friend_owner = ? \
                          AND friend = ?', (friend_owner_id, friend_id))

def get_all_profile_public_posts(cursor, user_id):
    cursor.execute(
       'SELECT  users.user_id, title, text_body, fname \
        FROM users JOIN creates_post \
        ON creates_post.user_id = users.user_id \
        JOIN post \
        ON post.post_id = creates_post.post_id \
        JOIN profile \
        ON profile.user_id = users.user_id \
        JOIN profile_info \
        ON profile.email = profile_info.email \
        WHERE users.user_id = ? \
        UNION \
        SELECT friend_owner as user_id, title, text_body, fname \
        FROM friend_of JOIN creates_post \
        ON friend_of.friend_owner = creates_post.user_id \
        JOIN post \
        ON post.post_id = creates_post.post_id \
        JOIN profile \
        ON profile.user_id = friend_of.friend_owner \
        JOIN profile_info \
        ON profile.email = profile_info.email \
        WHERE friend_of.friend = ?;', (user_id, user_id)
        )
    posts = cursor.fetchall()
    if posts:
      print posts
      return posts
