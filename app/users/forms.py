from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, EqualTo, Email
from app import db
from app.users.models import User

class LoginForm(Form):
  email = TextField('Email address', [DataRequired(), Email()])
  password = PasswordField('Password', [DataRequired()])

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    self.user = None

  def validate(self):
    rv = Form.validate(self)
    if not rv:
      return False

    user = self.get_user()

    if user is None:
      self.email.errors.append('Email or password was incorrect.')
      return False

    if user.password != self.password.data:
      self.password.errors.append('Email or password was incorrect.')
      return False

    self.user = user
    return True

  def get_user(self):
    print self.email.data
    return db.session.query(User).filter_by(email=self.email.data).first()

class RegistrationForm(Form):
  email = TextField('Email address', [DataRequired(), Email()])
  password = PasswordField('Password', [DataRequired()])
  confirm = PasswordField('Repeat Password', [
      DataRequired(),
      EqualTo('password', message='Passwords must match')
      ])

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    self.user = None

  def validate(self):
    rv = Form.validate(self)
    if not rv:
      return False

    if db.session.query(User).filter_by(email=self.email.data).count() > 0:
      self.email.errors.append('Account already exists')
      return False

    return True

  def get_user(self):
    print self.email.data
    return db.session.query(User).filter_by(email=self.email.data).first()
