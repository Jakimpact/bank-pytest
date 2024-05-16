import pytest

from app.bank import Account, Transaction


def test_deposit(session_isolated, account_factory):
    account1 = account_factory(session_isolated, "Q")
    account1.deposit(100)
    assert account1.balance == 100

# @pytest.mark.skip(reason="Not working")
# @pytest.mark.parametrize(("name, expected_name", [("Q", "Q"), ("L", "L")]))
# def test_multiple_creation(name, expected_name, session_isolated, account_factory):
#     account_factory(session_isolated, name)
#     assert len(session_isolated.query(Account).all()) == 3