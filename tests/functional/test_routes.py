from iebank_api import app, db
import pytest

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

# GET
def test_get_accounts(testing_client, add_account):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid and includes accounts
    """
    # Add a test account
    add_account('ironman', '€', 'Italy')

    response = testing_client.get('/accounts')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['accounts']) > 0  # Ensure there's at least one account

# POST
def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'ironman', 'currency': '€', 'country': 'Italy'})
    assert response.status_code == 200

    # Check if the response contains the newly created account
    data = response.get_json()
    assert data['name'] == 'ironman'
    assert data['currency'] == '€'
    assert data['country'] == 'Italy'

# POST2
def test_create_account2(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page receives a POST request
    THEN check that a code 200 is returned with the newly created account information
    """
    with app.app_context():
        db.create_all()  # Ensure you're in the app context when interacting with the database
        response = testing_client.post('/accounts', json={
            'name': 'Test Account',
            'currency': '€',
            'country': 'Italy'
        })
        assert response.status_code == 200
        assert response.json['name'] == 'Test Account'
        assert response.json['currency'] == '€'
        assert response.json['country'] == 'Italy'

# PUT
def test_update_account(testing_client, add_account):
    """
    GIVEN a Flask application
    WHEN an account is updated (PUT)
    THEN check the account fields are updated correctly
    """
    # Add a test account
    account = add_account('ironman', '€', 'Italy')

    response = testing_client.put(f'/accounts/{account.id}', json={
        'name': 'ironman Updated',
        'balance': 100.0
    })
    assert response.status_code == 200

    # Check if the account was updated
    data = response.get_json()
    assert data['name'] == 'ironman Updated'
    assert data['balance'] == 100.0

# DELETE
def test_delete_account(testing_client, add_account):
    """
    GIVEN a Flask application
    WHEN an account is deleted (DELETE)
    THEN check the account is removed from the database
    """
    # Add a test account
    account = add_account('thor', '€', 'spain')
    assert account is not None  # Ensure account was created

    response = testing_client.delete(f'/accounts/{account.id}')
    assert response.status_code == 200

    # Ensure the account was deleted
    response = testing_client.get(f'/accounts/{account.id}')
    assert response.status_code == 404

def test_get_non_existent_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a non-existent account is requested (GET)
    THEN check the response is 404
    """
    response = testing_client.get('/accounts/9999')  # Non-existent ID
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Account not found'


def test_update_non_existent_account(testing_client):
    """
    GIVEN a Flask application
    WHEN an update request is made for a non-existent account (PUT)
    THEN check the response is 404
    """
    response = testing_client.put('/accounts/9999', json={'name': 'Updated Name', 'balance': 100.0})
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Account not found'


def test_delete_non_existent_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a delete request is made for a non-existent account (DELETE)
    THEN check the response is 404
    """
    response = testing_client.delete('/accounts/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Account not found'