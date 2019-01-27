from app import app, db

class Auction(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    start = db.Column(db.String(120))
    stop = db.Column(db.String(120))
    item = db.Column(db.String(120))
    owner = db.Column(db.String(120))

    def __init__(self, title, start, stop, item, owner):
        self.title = title
        self.start = start
        self.stop = stop
        self.item = item
        self.owner = owner

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    owner = db.Column(db.String(120))

    def __init__(self, amount, auction_id, owner):
        self.amount = amount
        self.auction_id = auction_id
        self.owner = owner