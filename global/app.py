import os
import requests
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hash

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['host'] = "0.0.0.0"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from model import User, UserTransactions

ADDRESS = "http://192.168.43.122:5000/add/"


@app.route('/')
def hello_world():
    return '!! GLOBAL WALLET !!'


@app.route('/global/balance/<uid>')
def get_balance(uid):
    try:
        user = User.query.filter_by(username=uid).first()
        return {"message": "SUCCESS", "data": user.balance}
    except Exception as e:
        print(e)
        return {"message": "FAIL"}


@app.route('/global/add', methods=['POST'])
def add_money():
    if request.method == 'POST':
        service = request.form.get('service')
        sender_mail = request.form.get('sender_username')
        receiver_username = request.form.get('receiver_username')
        amount = request.form.get('amount')

        try:
            user = User.query.filter_by(username=receiver_username).first()

            if not user:
                raise Exception("User not found")

            user.balance += float(amount)

            user_transaction = UserTransactions(
                user_id=user.id,
                amount=amount,
                other_id=sender_mail,
                service=service,
                add=True,
                timestamp=datetime.now(tz=None)
            )
            db.session.add(user_transaction)
            db.session.commit()
            return {"message": "SUCCESS"}

        except Exception as e:
            db.session.rollback()
            print(str(e))
            return {"message": "FAIL"}

    else:
        return {"message": "Opps!! this only works in POST mode"}


@app.route('/global/decrease', methods=['POST'])
def dec_money():
    if request.method == 'POST':
        service = 'PAYTM'
        sender_username = request.form.get('sender_id')
        receiver_username = request.form.get('receiver_id')
        amount = request.form.get('amount')

        #sender_username = request.json['sender_id']
        #receiver_username = request.json['receiver_id']
        #amount = request.json['amount']

        try:
            user = User.query.filter_by(username=sender_username).first()

            if not user:
                raise Exception("User not found")
            if user.balance < float(amount):
                raise Exception("Insufficient Balance")

            user.balance -= float(amount)

            user_transaction = UserTransactions(
                user_id=user.id,
                amount=amount,
                other_id=receiver_username,
                service=service,
                add=False,
                timestamp=datetime.now(tz=None)
            )
            db.session.add(user_transaction)
            db.session.commit()
            url = ADDRESS+sender_username+"/"+receiver_username+"/"+amount
            r = requests.get(url=url)
            result = r.json()
            if result['status'] == 'SUCCESS':
                return {"message": "SUCCESS"}
            else:
                raise Exception('Error from Paytm')

        except Exception as e:
            db.session.rollback()
            print(str(e))
            return {"message": "FAIL"}

    else:
        return {"message": "Opps!! this only works in POST mode"}


@app.route('/global/inter', methods=['POST'])
def inter_money():
    if request.method == 'POST':
        service = 'GLOBAL'
        sender_username = request.form.get('sender_id')
        receiver_username = request.form.get('receiver_id')
        amount = request.form.get('amount')

        try:
            s_user = User.query.filter_by(username=sender_username).first()
            r_user = User.query.filter_by(username=receiver_username).first()

            if not s_user or not r_user:
                raise Exception("Either of User not found")
            if s_user.balance < float(amount):
                raise Exception("Insufficient Balance")

            s_user.balance -= float(amount)
            r_user.balance += float(amount)

            user_transaction = UserTransactions(
                user_id=s_user.id,
                amount=amount,
                other_id=r_user.email,
                service=service,
                add=False,
                timestamp=datetime.now(tz=None)
            )
            db.session.add(user_transaction)

            user_transaction = UserTransactions(
                user_id=r_user.id,
                amount=amount,
                other_id=s_user.email,
                service=service,
                add=True,
                timestamp=datetime.now(tz=None)
            )
            db.session.add(user_transaction)

            db.session.commit()
            return {"message": "SUCCESS"}

        except Exception as e:
            db.session.rollback()
            print(str(e))
            return {"message": "FAIL"}

    else:
        return {"message": "Opps!! this only works in POST mode"}


@app.route('/global/get/<uid>', methods=['GET'])
def get_transaction_details(uid):
    try:
        user = User.query.filter_by(username=uid).first()
        user_transaction = UserTransactions.query.filter_by(user_id=user.id).all()
        response = []
        for i in user_transaction:
            res = i.serialize()
            response.append(res)
        response = response[::-1]
        return {"message": "SUCCESS", "data": jsonify(response).json}
    except Exception as e:
        print(e)
        return {"message": "FAIL"}


#####################
#    USER AUTH      #
#####################
@app.route("/global/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get('uid')
        password = request.form.get('password')
        remember = False
        try:
            user = User.query.filter_by(username=username).first()

            if not user or not check_password_hash(user.password, password):
                raise Exception("Email or Password error")
            login_user(user, remember=remember)
            session = hash.hash_code(30)
            user.hash = session

            db.session.commit()
            return {"message": "SUCCESS", "session": session, "uid": user.username}

        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message": "FAIL"}

    return {"message": "You have reached here NICE!!!!"}


@app.route("/global/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        username = request.form.get('uid')
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                raise Exception("Email Id Used")
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password, method='sha256'),
                balance=1000.0,
                username=username
            )
            db.session.add(new_user)
            db.session.commit()
            return {"message": "SUCCESS"}

        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message": "FAIL"}

    return {"message": "You have reached here NICE!!!!"}


@app.route("/global/logout/")
def logout():
    usr = current_user.id
    try:
        user = User.query.get(usr)
        user.hash = ""
        db.session.commit()
        logout_user()
        return {"message": "SUCCESS"}
    except Exception as e:
        db.session.rollback()
        print(e)
        return {"message": "FAIL"}


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run()
