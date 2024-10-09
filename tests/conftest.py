import pytest
from iebank_api.models import Account
from iebank_api import db, app

## run tests: python -m pytest tests/
## run tests with coverage: python -m pytest --cov=iebank_api tests/


@pytest.fixture
def add_account():
    def _add_account(name, currency, country="Italy"):
        account = Account(name, currency, country)
        db.session.add(account)
        db.session.commit()
        return account
    return _add_account

@pytest.fixture(scope='module')  # Adjust scope as needed (function, module, session)
def testing_client():
    # Setup: Create the application context and the database
    with app.app_context():
        db.create_all()  # Create all tables
        yield app.test_client()  # This is where the tests run
        db.session.remove()  # Clean up session
        db.drop_all()  # Drop all tables after the tests
