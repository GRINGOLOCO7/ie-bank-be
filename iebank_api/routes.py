from flask import Flask, request, render_template
from iebank_api import db, app
from iebank_api.models import Account


account_structure = {
    'id': 'int',
    'name': 'str',
    'account_number': 'str',
    'balance': 'float',
    'currency': 'str',
    'status': 'str',
    'created_at': 'datetime',
    'country': 'str'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accounts', methods=['POST'])
def create_account():
    name = request.json['name']
    currency = request.json['currency']
    account = Account(name, currency)
    db.session.add(account)
    db.session.commit()
    return format_account(account)

@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return {'accounts': [format_account(account) for account in accounts]}

@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    account.name = request.json['name']
    account.balance = request.json['balance']
    db.session.commit()
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['DELETE'])
def add_field():
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    return format_account(account)

def format_account(account):
    global account_structure
    for key in account_structure:
        if key == 'id':
            account_structure[key] = account.id
        elif key == 'name':
            account_structure[key] = account.name
        elif key == 'account_number':
            account_structure[key] = account.account_number
        elif key == 'balance':
            account_structure[key] = account.balance
        elif key == 'currency':
            account_structure[key] = account.currency
        elif key == 'status':
            account_structure[key] = account.status
        elif key == 'created_at':
            account_structure[key] = account.created_at
        elif key == 'country':
            account_structure[key] = account.country
    return account_structure







#################################################################




@app.route('/skull', methods=['GET'])
def skull():
    text = 'Hi! This is the BACKEND SKULL! 💀 '

    text = text +'<br/>Database URL:' + db.engine.url.database
    if db.engine.url.host:
        text = text +'<br/>Database host:' + db.engine.url.host
    if db.engine.url.port:
        text = text +'<br/>Database port:' + db.engine.url.port
    if db.engine.url.username:
        text = text +'<br/>Database user:' + db.engine.url.username
    if db.engine.url.password:
        text = text +'<br/>Database password:' + db.engine.url.password
    return text