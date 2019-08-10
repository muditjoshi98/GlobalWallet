from app import db
import datetime


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, sender_id, receiver_id, amount):
        self.receiver_id = receiver_id
        self.service = service
        self.amount = amount
        self.sender_id = sender_id
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'amount': self.amount,
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    service = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, email, password, name, username, balance, service):
        self.email = email
        self.password = password
        self.name = name
        self.username = username
        self.balance = balance
        self.service = service

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'balance': self.balance,
            'service': self.service
        }

class OuterTransaction(db.Model):
    __tablename__ = 'outer_transaction'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(80), nullable=False)
    receiver_id = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, sender_id, receiver_id, amount):
        self.receiver_id = receiver_id
        self.amount = amount
        self.sender_id = sender_id
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'amount': self.amount,
        }
        

