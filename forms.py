"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from wtforms import Form, validators, TextField, PasswordField, SelectField


class LoginForm(Form):
    email = TextField(u'Username', validators=[validators.Required()])
    password = PasswordField(u'Password', validators=[validators.Required()])

class AddFriendForm(Form):
    friend = TextField(u'Friend', validators=[validators.Required()])
    category = SelectField(u'Category', choices=[('Relative','Relative'),
                                                 ('School','School'),
                                                 ('Work','Work')])
