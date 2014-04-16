"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from functools import wraps
import os

from flask import Flask, render_template, request, redirect, url_for, session, \
     escape
import oursql
import werkzeug

import db
from forms import LoginForm, AddFriendForm, SignupForm, CreateGroupForm

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY',
    'qi2pQ)#RNF<x!t/}Ra30J9g~XO+OW$jPn%4R{P8}3lbU;0|%s>K]_*K|Q(+kQNHS')
app.jinja_env.add_extension('pyhaml_jinja.HamlExtension')


def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None or db.get_user_profile(db.conn.cursor(oursql.DictCursor), user_id) is None:
            return redirect(url_for('login'))

        return f(*args, **kwargs)
    return decorated_view


###
# Routing for your application.
###


@app.route('/')
@login_required
def home():
    return profile_page()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate():
        cursor = db.conn.cursor(oursql.DictCursor)
        user = db.authenticate(cursor, form.email.data, form.password.data)
        if user is None:
            return render_template('login.haml',
                                   form=form,
                                   error='Invalid login')

        session['user_id'] = user['user_id']
        return redirect(url_for('profile_page'))

    return render_template('login.haml')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)

    if request.method == 'POST' and form.validate():
        cursor = db.conn.cursor(oursql.DictCursor)
        user = db.signup(cursor, form.fname.data, form.lname.data,
                         form.email.data, form.password.data,
                         form.mar_stat.data, form.dob.data)

        return redirect(url_for('login'))

    return render_template('signup.haml')


@login_required
@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.haml')

@app.route('/group_panel')
@login_required
def group_panel():
    return render_template('group_panel.haml')

@login_required
@app.route('/profile_page')
def profile_page():
    cursor = db.conn.cursor(oursql.DictCursor)
    user = db.get_user_profile(cursor, escape(session.get('user_id')))
    posts = db.get_all_profile_public_posts(cursor,
                                            escape(session['user_id']))
    return render_template('profile_page.haml', user=user, posts=posts)

@login_required
@app.route('/add_friend', methods=['POST'])
def add_friend():
    form = AddFriendForm(request.form)
    if form.validate():
        cursor = db.conn.cursor(oursql.DictCursor)
        email = form.friend.data
        category = form.category.data
        friend_id = db.get_id_by_email(cursor, email)
        db.add_friend(cursor, escape(session['user_id']), friend_id['user_id'],
                      category)

    return redirect(url_for('profile_page'))

@app.route('/create_reports', methods=['POST'])
def create_reports():
    cursor = db.conn.cursor(oursql.DictCursor)
    report1 = db.get_admin_report_friends(cursor)
    report2 = db.get_admin_report_comments(cursor)
    report3 = db.get_admin_report_posts(cursor)
    report4 = db.get_admin_report_gposts(cursor)
    return render_template('admin.haml', report1=report1, report2=report2,
                                         report3=report3, report4=report4)

@app.route('/create_group', methods=['POST'])
def create_group():
    form = CreateGroupForm(request.form)
    if form.validate():
        cursor = db.conn.cursor(oursql.DictCursor)
        group_name = form.group_name.data
        if db.user_created_group(cursor, escape(session['user_id'])):
            return redirect(url_for('profile_page'))
        db.create_group(cursor, escape(session['user_id']), group_name)

    return redirect(url_for('profile_page'))

@app.route('/admin')
def admin_page():
    return render_template('admin.haml')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    file = request.files['file']
    if file:
        filename = werkzeug.secure_filename(file.filename)
        file.save(os.path.join(os.path.join(os.getcwd(), 'uploads'), filename))
        return redirect(url_for('profile_page', filename=filename))

    return 500

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
