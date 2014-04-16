import os
import re
import urlparse

import oursql


conn = oursql.connect(
   host='localhost', user='root', passwd='', db='mybook')


def signup(cursor,fname, lname, email, password, marital_status, dob):
   cursor.execute(
      'INSERT INTO users (hpassword, martial_status) values(?,?),',
      (password, marital_status))
   cursor.execute(
     'INSERT INTO profile_info (fname,lname,email,dob) values(?,?,?,?)'
      (fname, lname, email, dob))
   return True

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
        'SELECT * FROM profile_info WHERE profile.user_id = ?',
        (user_id))
    user = cursor.fetchone()
    if user:
      return user

def get_user_proifle_pic(cursor,user_id):
   cursor.execute('SELECT profile_pic_path FROM profile_pic WHERE user_id =?',
                  (user_id))
   return True

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
            except (oursql.OperationalError, oursql.ProgrammingError) as e:
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
    cursor.execute(
        'SELECT user_id FROM profile WHERE profile.email = ?;',
        (email))
    user = cursor.fetchone()
    if user:
      return user

def add_friend(cursor, friend_owner_id, friend_id, category):
    cursor.execute('CALL add_friend(?,?,?);',
                   (friend_owner_id, friend_id, category))
    return True

def create_group(cursor, owner_id, group_name):
    cursor.execute('CALL create_group(?,?);',
                   (owner_id, group_name))
    return True

def user_created_group(cursor,owner_id):
    cursor.execute('Select * from create_group where create_group.user_id=?;',
                   (owner_id))
    user = cursor.fetchone()
    if user:
      return True
    return False

def remove_friend(friend_owner_id, friend_id):
    return cursor.execute('DELETE FROM friend_of WHERE friend_owner = ? \
                          AND friend = ?', (friend_owner_id, friend_id))

def add_editor_group(cursor, group_owner, user_added):
   cursor.execute('INSERT INTO add_editors_group (group_owner,user_added) values(?,?, NOW())',
                  (group_owner, user_added))
   return True

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
