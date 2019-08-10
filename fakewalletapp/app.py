import os
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from constants import Constants
import requests

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from model import Transaction, User, OuterTransaction

#Team.no. 24
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if check_password_hash(user.password, password):
        return {'status':'SUCCESS', 'uid':str(user.id)}
    else:
        return {'status':'FAILURE'}

@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        email = request.json['email']
        password = request.json['password']
        name = request.json['name']
        username = request.json['username']
        service = request.json['service']

        user = User.query.filter_by(email=email).first()
        if user:
            return {"status": "Email already exists"}
        else:
            new_user = User(
                email=email,
                name=name,
                username=username,
                service=service,
                password=generate_password_hash(password, method='sha256'),
                balance=10.0
            )
        db.session.add(new_user)
        db.session.commit()
        return {"status": "SUCCESS"}

@app.route("/logout/")
def logout():
    return {"status": "SUCCESS"}

if __name__ == '__main__':
    app.run()

@app.route("/pay/<uid>/<gl_uid>/<amt>")
def pay(uid, gl_uid, amt):
    amt = float(amt)
    ip = '192.168.43.59:5000'
    url = 'http://{}/global/add'.format(ip)
    user = User.query.filter_by(id = uid).first()
    if user.balance < amt:
        return {'status':'FAILURE', 'message': 'Insufficient balance'}
    payload = {'sender_username': user.email, 'receiver_username': gl_uid, 'amount': amt, 'service': 'PAYTM'}
    r = requests.post(url = url, data = payload)
    result = r.json()
    if result['message'] == 'SUCCESS':
        user.balance = user.balance - amt
        db.session.commit()
        transaction = OuterTransaction(sender_id = str(uid), receiver_id = str(gl_uid), amount = amt)
        db.session.add(transaction)
        db.session.commit()
        return {'status':'SUCCESS'}
    else:
        return {'status':'FAILURE'}
    
@app.route("/add/<gl_username>/<username>/<amt>")
def add_money(gl_username, username, amt):
    print(request.url)
    amt = float(amt)
    user = User.query.filter_by(username = username).first()
    if not user:
        return {"status": "FAILURE"}
    else:
        user.balance = user.balance + amt
        transaction = OuterTransaction(sender_id = str(gl_username), receiver_id = str(user.id), amount = amt)
        db.session.add(transaction)
        db.session.commit()
        return {"status": "SUCCESS"}

@app.route("/balance/<uid>")
def balance(uid):
    user = User.query.filter_by(id = int(uid)).first()
    if user:
        return {"status": "SUCCESS", "balance": str(user.balance)}
    else:
        return {"status": "FAILURE"}

@app.route("/loginandpay", methods=["POST"])
def loginandpay():
    username = request.form.get('username')
    password = request.form.get('password')
    gl_uid = request.form.get('gl_username')
    amt = request.form.get('amount')
    user = User.query.filter_by(username=username).first()
    if not user or (not check_password_hash(user.password, password)):
        return {'status':'FAILURE'}
    else:
        uid = user.id
        result = pay(uid, gl_uid, amt)
        if result['status'] == 'SUCCESS':
            return {'status':'SUCCESS', 'uid':user.id}
        else:
            return {"status": "FAILURE"}

@app.route("/loginandbalance", methods=["POST"])
def loginandbalance():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or (not check_password_hash(user.password, password)):
        return {'status':'FAILURE'}
    else:
        return balance(user.id)


