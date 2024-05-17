from mock_alchemy.mocking import UnifiedAlchemyMagicMock
import pytest

from app.bank import Account


@pytest.fixture(scope="function")
def session_function():
    session = UnifiedAlchemyMagicMock()
    yield session
    session.rollback()

@pytest.fixture(scope="module")
def session_module():
    session = UnifiedAlchemyMagicMock()
    yield session
    session.rollback()

@pytest.fixture(scope="session")
def session_global():
    session = UnifiedAlchemyMagicMock()
    yield session
    session.rollback()

@pytest.fixture
def account_factory():
    def create_account(session, name, balance=0):
        return Account(session=session, name=name, balance=balance)
    return create_account