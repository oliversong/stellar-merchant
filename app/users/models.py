from app import db
from app.users import constants as USER

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(120))
  email = db.Column(db.String(120))
  authToken = db.Column(db.String(150))
  updateToken = db.Column(db.String(150))
  secret = db.Column(db.String(150))
  address = db.Column(db.String(150))
  role = db.Column(db.SmallInteger, default=USER.USER)
  status = db.Column(db.SmallInteger, default=USER.NEW)

  def __init__(self, username, password, email, authToken, updateToken, secret, address):
    self.username = username
    self.password = password
    self.email = email
    self.authToken = authToken
    self.updateToken = updateToken
    self.secret = secret
    self.address = address

  def getStatus(self):
    return USER.STATUS[self.status]

  def getRole(self):
    return USER.ROLE[self.role]

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<User %r>' % (self.username)
