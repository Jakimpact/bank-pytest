import pytest

from app.bank import Account, Transaction


def test_deposit_normal(session_isolated, account_factory):
    account1 = account_factory(session_isolated, "Q")
    account1.deposit(100)
    transaction = session_isolated.query(Transaction).first()
    assert account1.balance == 100
    assert len(session_isolated.query(Transaction).all()) == 1
    assert transaction.type == "deposit"
    session_isolated.commit.assert_called()

def test_deposit_negative_amount(session_isolated, account_factory):
    account1 = account_factory(session_isolated, "Q")
    with pytest.raises(ValueError):
        account1.deposit(-100)
    assert account1.balance == 0
    assert len(session_isolated.query(Transaction).all()) == 0
    session_isolated.commit.assert_called()

def test_deposit_zero_amount(session_isolated, account_factory):
    account1 = account_factory(session_isolated, "Q")
    with pytest.raises(ValueError):
        account1.deposit(0)
    assert account1.balance == 0
    assert len(session_isolated.query(Transaction).all()) == 0
    session_isolated.commit.assert_called()