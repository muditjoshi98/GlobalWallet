from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    password = db.Column(db.String(), nullable=False)
    hash = db.Column(db.String(30))

    def __init__(self, email, password, name, balance, username):
        self.email = email
        self.password = password
        self.name = name
        self.balance = balance
        self.username = username

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'balance': self.balance
        }


class UserTransactions(db.Model):
    __tablename__ = 'user_transaction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    other_id = db.Column(db.String, nullable=False)
    service = db.Column(db.String, nullable=False)
    add = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, amount, other_id, add, timestamp, service):
        self.user_id = user_id
        self.amount = amount
        self.other_id = other_id
        self.add = add
        self.timestamp = timestamp
        self.service = service

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'amount': str(self.amount),
            'other_id': str(self.other_id),
            'add': str(self.add),
            'service': str(self.service),
            'timestamp': str(self.timestamp)
        }

