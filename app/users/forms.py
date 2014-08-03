from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, EqualTo
from app import db
from app.users.models import User
import pyscrypt
import requests
import json
import base64
from Crypto.Cipher import AES
import binascii

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
      print "auth with server"
      r = requests.post(url, data=json.dumps(payload), headers=headers)
      if r.ok:
        # check if successful
        # decrypt information
        payload = {"id":hashed, "username":self.username.data, "password":self.password.data, "content": r.content}
        print "send decrypt request to node service"
        r = requests.post("http://127.0.0.1:3000/decrypt", data=json.dumps(payload), headers=headers)
        response = json.loads(r.text)
        print response
        # create account
        mainData = json.loads(response['mainData'])
        keychainData = json.loads(response['keychainData'])
        u = User(
           username=self.username.data,
           password=self.password.data,
           email=mainData['email'],
           authToken=keychainData['authToken'],
           updateToken=keychainData['updateToken'],
           secret=keychainData['signingKeys']['secret'],
           address=keychainData['signingKeys']['address']
        )
        db.session.add(u)
        db.session.commit()
        self.user = user
        return True
      else:
        self.password.errors.append('Username or password was incorrect.')
        return False

    if user.password != self.password.data:
      self.password.errors.append('Username or password was incorrect.')
      return False

    self.user = user
    return True

  def derive_id(self, username, password):
    credentials = (username.lower() + password).encode('ascii',errors='backslashreplace')
    salt = credentials.encode('ascii',errors='backslashreplace')
    hashed = pyscrypt.hash(credentials, salt, 2048, 8, 1, 32)
    return hashed.encode('hex')

  def get_user(self):
    return db.session.query(User).filter_by(username=self.username.data).first()
