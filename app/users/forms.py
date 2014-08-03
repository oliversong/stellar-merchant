from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, EqualTo
from app import db
from app.users.models import User
import pyscrypt
import requests
import json

class LoginForm(Form):
  username = TextField('Username', [DataRequired()])
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
      # scrypt hash then query API for user
      hashed = self.derive_id(self.username.data, self.password.data)
      payload = {"id": hashed}
      url = 'https://wallet.stellar.org/wallets/show'
      headers = {'content-type': 'application/json'}
      r = requests.post(url, data=json.dumps(payload), headers=headers)
      print(r.text)
      return False

    if user.password != self.password.data:
      self.password.errors.append('Username or password was incorrect.')
      return False

    self.user = user
    return True

  def get_user(self):
    return db.session.query(User).filter_by(username=self.username.data).first()

  def derive_id(self, username, password):
    credentials = (username.lower() + password).encode('ascii',errors='backslashreplace')
    salt = credentials.encode('ascii',errors='backslashreplace')

    hashed = pyscrypt.hash(credentials, salt, 2048, 8, 1, 32)

    return hashed.encode('hex')
