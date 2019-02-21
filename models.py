from app import app, db
from datetime import datetime

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    items = db.relationship('Item', backref='owner', lazy='dynamic')
    bids = db.relationship('Bid', backref='owner', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    start = db.Column(db.DateTime, nullable = False)
    stop = db.Column(db.DateTime, nullable = False)
    description = db.Column(db.String(455))
    bids = db.relationship('Bid', backref='item-bids', lazy='dynamic')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, start, stop, description, owner_id):
        self.title = title
        self.start = start
        self.stop = stop
        self.description = description
        self.owner_id = owner_id


class Bid(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, amount, item_id, owner_id, timestamp):
        self.amount = amount
        self.item_id = item_id
        self.owner_id = owner_id


        






        