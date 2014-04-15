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
