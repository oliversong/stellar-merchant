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
      r = requests.post(url, data=json.dumps(payload), headers=headers)
      print "auth with server"
      payload = {"id":hashed, "username":self.username.data, "password":self.password.data, "content": r.content}
      print "send decrypt request to node service"
      r = requests.post("http://127.0.0.1:3000/decrypt", data=json.dumps(payload), headers=headers)
      # key = self.derive_key(hashed, self.username.data, self.password.data)
      # content = json.loads(r.content)['data']
      # wallet = self.decrypt_this(content, hashed, key)
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

  def derive_key(self, id, username, password):
    credentials = (id + username.lower() + password).encode('ascii',errors='backslashreplace')
    salt = credentials.encode('ascii',errors='backslashreplace')
    hashed = pyscrypt.hash(credentials, salt, 2048, 8, 1, 32)
    return hashed

  def decrypt_this(self, encrypted, id, key):
    mainData = self.decrypt_data(encrypted['mainData'], key)
    keychainData = self.decrypt_data(encrypted['keychainData'], key)

    options = {
      "id": id,
      "key": key,
      "mainData": mainData,
      "keychainData": keychainData
    }

    return options

  def decrypt_data(self, encrypted, key):
    headers = {'content-type': 'application/json'}
    r = requests.post("http://127.0.0.1:3000/decrypt", data=json.dumps({"encrypted":encrypted,"key":key}), headers=headers)
    # FML
    # decoded = json.loads(base64.b64decode(encrypted))
    # raw_cipher = base64.b64decode(decoded['cipherText'])
    # raw_IV = binascii.a2b_base64(decoded['IV'])
    # cipher_name = decoded['cipherName'];
    # mode = decoded['mode'];
    # # Decrypt the data in CCM mode using AES and the given IV.
    # cipher = AES.new(binascii.unhexlify(key), AES.MODE_ECB, raw_IV)
    # data = cipher.decrypt(unpad(raw_cipher))
    raise Exception("WOO")
