import pytest

from app.bank import Account, Transaction


def test_create_account(session_isolated, account_factory):
    account1 = account_factory(session_isolated, "Q")
    assert account1.name == "Q"
    session_isolated.commit.assert_called()

def test_create_multiple_account(session_isolated, account_factory):
    account_factory(session_isolated, "Q")
    account_factory(session_isolated, "L")
    account_factory(session_isolated, "J")
    assert len(session_isolated.query(Account).all()) == 3
    session_isolated.commit.assert_called()

@pytest.mark.session
def test_create_accounts(session_shared, account_factory):
    account1 = account_factory(session_shared, "Q")
    account2 = account_factory(session_shared, "L")
    account3 = account_factory(session_shared, "J")
    account4 = account_factory(session_shared, "K")
    assert len(session_shared.query(Account).all()) == 4

@pytest.mark.session
def test_shared2(session_shared, account_factory):
    account5 = account_factory(session_shared, "E")
    assert len(session_shared.query(Account).all()) == 5

@pytest.mark.skip(reason="WIP")
@pytest.mark.session
def test_modify_accounts(session_shared, account_factory):
    session_shared.query(Account).filter(Account.name=="E").delete()
    assert len(session_shared.query(Account).all()) == 4