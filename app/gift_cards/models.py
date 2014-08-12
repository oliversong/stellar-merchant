from app import db

class GiftCard(db.Model):
    __tablename__ = 'giftcards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    cost = db.Column(db.String(120))
    credit = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, cost, credit):
        self.name = name
        self.cost = cost
        self.credit = credit

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Gift Card %r>' % (self.name)
