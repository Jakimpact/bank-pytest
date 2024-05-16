import pytest

from app.bank import Account, Transaction


# @pytest.mark.skip(reason="Not working")
# @pytest.mark.parametrize(("name, expected_name", [("Q", "Q"), ("L", "L")]))
# def test_multiple_creation(name, expected_name, session_isolated, account_factory):
#     account_factory(session_isolated, name)
#     assert len(session_isolated.query(Account).all()) == 3