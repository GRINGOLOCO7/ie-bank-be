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
    country = request.json['country']
    account = Account(name, currency, country)
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
    if account is None:
        return {'error': 'Account not found'}, 404  # Return a proper error message
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    if account is None:  # Check if the account exists
        return {'error': 'Account not found'}, 404
    account.name = request.json['name']
    account.balance = request.json['balance']
    db.session.commit()
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    if account is None:
        return {'error': 'Account not found'}, 404

    db.session.delete(account)
    db.session.commit()
    return {'message': 'Account deleted'}, 200

def format_account(account):
    if account is None:
        return {'error': 'Account not found'}

    formatted_account = {
        'id': account.id,
        'name': account.name,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'status': account.status,
        'created_at': account.created_at,
        'country': account.country
    }
    return formatted_account






#################################################################


@app.route('/update')
def update():
    return render_template('update.html')

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