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
class SignupForm(Form):
     fname = TextField(u'Firstname', validators=[validators.Required()])
     lname = TextField(u'Lastname', validators=[validators.Required()])
     mar_stat = TextField(u'Mar_stat', choices=[('Married', 'Married'),
                                                       ('Single','Single'),
                                                       ('Divorced', 'Divorced'),
                                                       ('Widowed', 'Widowed')])
     email = TextField(u'email', validators=[validators.Required()])
     password = PasswordField(u'Password', validators=[validators.Required()])
     
 
